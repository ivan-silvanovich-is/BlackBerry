import json
import os

from django.apps import apps
from django.core import serializers
from django.core.management.commands import loaddata
from django.db import connections


def should_add_record(record):
    arr = record['model'].split('.')
    model_class = apps.get_model(app_label=arr[0], model_name=arr[1])
    return not model_class.objects.filter(id=record['pk']).exists()


def filter_fixtures(fixture_file, fixture_dir, fixture_name):
    # Read the original JSON file
    with open(fixture_file) as json_file:
        json_list = json.load(json_file)

    # Filter out records that already exists
    # json_list_filtered = list(filter(should_add_record, json_list))
    json_list_filtered = [record for record in json_list if should_add_record(record)]
    if not json_list_filtered:
        print(f"skip {fixture_file}")
        return None, None

    # Write the updated JSON file
    file_dir_and_name, file_ext = os.path.splitext(fixture_file)
    temp_fixture_label = f'{fixture_name}_temp.{file_ext}'
    temp_fixture_path = os.path.join(fixture_dir, temp_fixture_label)
    with open(temp_fixture_path, 'w') as json_file_temp:
        json.dump(json_list_filtered, json_file_temp)

    return temp_fixture_label, temp_fixture_path


class Command(loaddata.Command):
    def loaddata(self, fixture_labels):
        connection = connections[self.using]

        # Keep a count of the installed objects and fixtures
        self.fixture_count = 0
        self.loaded_object_count = 0
        self.fixture_object_count = 0
        self.models = set()

        self.serialization_formats = serializers.get_public_serializer_formats()


        # Django's test suite repeatedly tries to load initial_data fixtures
        # from apps that don't have any fixtures. Because disabling constraint
        # checks can be expensive on some database (especially MSSQL), bail
        # out early if no fixtures are found.
        fixtures_files = [self.find_fixtures(fixture_label) for fixture_label in fixture_labels]
        if not any(fixtures_files):
            return

        temp_fixture_labels_list = []
        temp_fixtures_path_list = []
        for fixture_sets in fixtures_files:
            for fixture_file, fixture_dir, fixture_name in fixture_sets:
                temp_fixture_label, temp_fixture_path = filter_fixtures(fixture_file, fixture_dir, fixture_name)

                if temp_fixture_label:
                    temp_fixture_labels_list.append(temp_fixture_label)
                    temp_fixtures_path_list.append(temp_fixture_path)

        fixture_labels = list(set(temp_fixture_labels_list))

        self.objs_with_deferred_fields = []
        with connection.constraint_checks_disabled():
            for fixture_label in fixture_labels:
                self.load_label(fixture_label)
            for obj in self.objs_with_deferred_fields:
                obj.save_deferred_fields(using=self.using)

        # Since we disabled constraint checks, we must manually check for
        # Since we disabled constraint checks, we must manually check for
        # any invalid keys that might have been added
        table_names = [model._meta.db_table for model in self.models]
        try:
            connection.check_constraints(table_names=table_names)
        except Exception as e:
            e.args = ("Problem installing fixtures: %s" % e,)
            raise

        # If we found even one object in a fixture, we need to reset the
        # database sequences.
        if self.loaded_object_count > 0:
            self.reset_sequences(connection, self.models)

        if self.verbosity >= 1:
            if self.fixture_object_count == self.loaded_object_count:
                self.stdout.write(
                    "Installed %d object(s) from %d fixture(s)"
                    % (self.loaded_object_count, self.fixture_count)
                )
            else:
                self.stdout.write(
                    "Installed %d object(s) (of %d) from %d fixture(s)"
                    % (
                        self.loaded_object_count,
                        self.fixture_object_count,
                        self.fixture_count,
                    )
                )

        # You can choose to not delete the file so that you can see what was added to your records
        for path in temp_fixtures_path_list:
            os.remove(path)

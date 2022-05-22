# test util

import logging
import sys
import unittest
from pathlib import Path
import shutil
import csv

# local
from py4ami.util import Util
from test.resources import Resources

logger = logging.getLogger("py4ami_test_util")

class TestUtil(unittest.TestCase):

    # def __init__(self):
    sys_argv_save = None

    @classmethod
    def setUp(cls):
        """save args as they will be edited"""
        cls.sys_argv_save = sys.argv

    @classmethod
    def tearDown(cls):
        """restore args"""
        sys.argv = cls.sys_argv_save

    @classmethod
    def test_add_argstr(cls):
        # this is a hack as normally there is only one element
        sys.argv = sys.argv[1:]
        assert sys.argv[1:] == []
        cmd = "foo bar plinge"
        Util.add_sys_argv_str(cmd)
        assert sys.argv[1:] == ["foo", "bar", "plinge"]

    @classmethod
    def test_add_args(cls):
        # this is a hack as normally there is only one element
        sys.argv = sys.argv[1:]
        assert sys.argv[1:] == []
        args = ["foox", "barx", "plingex"]
        Util.add_sys_argv(args)
        assert sys.argv[1:] == ["foox", "barx", "plingex"]

    @classmethod
    def test_copy_anything(cls):
        src = Resources.CLIMATE_10_SVG_DIR
        dst = Path(Resources.TEMP_DIR, "tempzz")
        if dst.exists():
            shutil.rmtree(dst)
        Util.copyanything(src, dst)
        assert Path(dst).exists()

    def test_create_name_value(self):
        """tests parsing of PyAMI flags
        """
        name, value = Util.create_name_value("foo=bar")
        assert name, value == ("foo", "bar")
        name, value = Util.create_name_value("foo")
        assert name, value == ("foo", True)
        try:
            arg = "foo=bar=plugh"
            Util.create_name_value(arg)
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve == "too many delimiters in {arg}")
        try:
            arg = "foo bar"
            n,v = Util.create_name_value(arg)
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve) == "arg [foo bar] may not contain whitespace"

        Util.create_name_value("foo/bar")
        assert name, value == ("foo/bar")

        Util.create_name_value("foo/bar", delim="/")
        assert name, value == ("foo", "bar")

        assert Util.create_name_value("") is None

        try:
            arg = "foo bar"
            n,v = Util.create_name_value(arg, delim=" ")
            raise ValueError(f"failed to trap {arg}")
        except ValueError as ve:
            assert str(ve) == f"arg [{arg}] may not contain whitespace"


    def test_read_csv(self):
        """use Python csv to select column values"""
        csv_file = Path(Resources.TEST_RESOURCES_DIR, "eoCompound", "compound_enzyme.csv")
        assert csv_file.exists(), f"{csv_file} should exist"
        with open(str(csv_file), newline='') as csvfile:
            row_values = [["isopentenyl diphosphate", "COMPOUND"],
                          ["dimethylallyl diphosphate", "COMPOUND"],
                          ["hemiterpene", "COMPOUND"]]
            reader = csv.DictReader(csvfile)

            for i, row in enumerate(reader):
                if i < 3:
                    assert row['NAME'] == row_values[i][0]
                    assert row['TYPE'] == row_values[i][1]

    def test_select_csv_field_by_type(self):
        """select value in column of csv file by value of defining column
        """
        csv_file = Path(Resources.TEST_RESOURCES_DIR, "eoCompound", "compound_enzyme.csv")
        assert csv_file.exists(), f"{csv_file} should exist"
        selector_column = "TYPE"
        column_with_values = "NAME"
        selector_value = "COMPOUND"

        values = Util.extract_csv_fields(csv_file, column_with_values, selector_column, selector_value)
        assert len(values) == 89
        assert values[:3] == ['isopentenyl diphosphate', 'dimethylallyl diphosphate', 'hemiterpene']

        selector_value = "ENZYME"
        values = Util.extract_csv_fields(csv_file, column_with_values, selector_column, selector_value)
        assert len(values) == 92
        assert values[:3] == ['isomerase', 'GPP synthase', 'FPP synthase']






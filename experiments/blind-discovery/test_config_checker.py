import unittest

from config_checker import validate


class ValidateConfigTests(unittest.TestCase):
    def test_reports_all_missing_keys(self):
        self.assertEqual(
            validate({}),
            '설정 오류: model, version 항목이 없습니다.',
        )

    def test_reports_only_model_when_model_is_missing(self):
        self.assertEqual(validate({'version': 'secret'}), '설정 오류: model 항목이 없습니다.')

    def test_reports_only_version_when_version_is_missing(self):
        self.assertEqual(validate({'model': 'secret'}), '설정 오류: version 항목이 없습니다.')

    def test_accepts_complete_config(self):
        self.assertEqual(validate({'model': 'secret', 'version': 'secret'}), '설정 정상')

    def test_does_not_include_config_values_in_error(self):
        result = validate({'version': 'sensitive-version'})
        self.assertNotIn('sensitive-version', result)


if __name__ == '__main__':
    unittest.main()

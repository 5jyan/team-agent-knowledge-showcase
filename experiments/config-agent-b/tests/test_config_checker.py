import unittest

from implementation.config_checker import check_config


class ConfigCheckerTests(unittest.TestCase):
    def test_reports_missing_model(self):
        self.assertEqual(
            check_config({"version": 1}),
            "설정 오류: model 항목이 없습니다",
        )

    def test_accepts_config_with_model(self):
        self.assertEqual(check_config({"model": "demo", "version": 1}), "설정 정상")

    def test_does_not_expose_configuration_values(self):
        secret = "do-not-print"
        message = check_config({"version": secret})
        self.assertNotIn(secret, message)

    def test_reports_both_missing_keys(self):
        self.assertEqual(
            check_config({}),
            "설정 오류: model, version 항목이 없습니다",
        )

    def test_reports_missing_version(self):
        self.assertEqual(
            check_config({"model": "demo"}),
            "설정 오류: version 항목이 없습니다",
        )


if __name__ == "__main__":
    unittest.main()

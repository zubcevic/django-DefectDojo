from ..dojo_test_case import DojoTestCase
from dojo.tools.nuclei.parser import NucleiParser
from dojo.models import Test
from datetime import datetime
from dateutil.tz import tzoffset


class TestNucleiParser(DojoTestCase):

    def test_parse_no_empty(self):
        testfile = open("unittests/scans/nuclei/empty.jsonl")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_no_findings(self):
        testfile = open("unittests/scans/nuclei/no_findings.json")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_many_findings(self):
        testfile = open("unittests/scans/nuclei/many_findings.json")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()

        self.assertEqual(16, len(findings))

        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("OpenSSH 5.3 Detection", finding.title)
            self.assertEqual("Low", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIn("network", finding.unsaved_tags)
            self.assertIn("openssh", finding.unsaved_tags)
            self.assertIsNotNone(finding.references)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(22, finding.unsaved_endpoints[0].port)
            self.assertEqual("openssh5.3-detect", finding.vuln_id_from_tool)

        with self.subTest(i=1):
            finding = findings[1]
            self.assertEqual("nginx version detect", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.unsaved_tags)
            self.assertIsNone(finding.references)
            self.assertEqual(None, finding.unsaved_endpoints[0].path)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(443, finding.unsaved_endpoints[0].port)
            self.assertEqual("nginx-version", finding.vuln_id_from_tool)

        with self.subTest(i=2):
            finding = findings[2]
            self.assertEqual("phpMyAdmin setup page", finding.title)
            self.assertEqual("Medium", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNotNone(finding.references)
            self.assertIn("phpmyadmin", finding.unsaved_tags)
            self.assertEqual("phpmyadmin/setup/index.php", finding.unsaved_endpoints[0].path)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(443, finding.unsaved_endpoints[0].port)
            self.assertEqual("phpmyadmin-setup", finding.vuln_id_from_tool)

        with self.subTest(i=3):
            finding = findings[3]
            self.assertEqual("Wappalyzer Technology Detection", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.references)
            self.assertIsNone(finding.unsaved_tags)
            self.assertEqual("WebGoat", finding.unsaved_endpoints[0].path)
            self.assertEqual("127.0.0.1", finding.unsaved_endpoints[0].host)
            self.assertEqual(8080, finding.unsaved_endpoints[0].port)
            self.assertEqual("tech-detect", finding.vuln_id_from_tool)

        with self.subTest(i=4):
            finding = findings[4]
            self.assertEqual("Wappalyzer Technology Detection", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(2, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.references)
            self.assertIsNone(finding.unsaved_tags)
            self.assertEqual("WebGoat", finding.unsaved_endpoints[0].path)
            self.assertEqual("127.0.0.1", finding.unsaved_endpoints[0].host)
            self.assertEqual(8080, finding.unsaved_endpoints[0].port)
            self.assertEqual("WebWolf", finding.unsaved_endpoints[1].path)
            self.assertEqual("127.0.0.1", finding.unsaved_endpoints[1].host)
            self.assertEqual(9090, finding.unsaved_endpoints[1].port)
            self.assertEqual("tech-detect", finding.vuln_id_from_tool)

        with self.subTest(i=12):
            finding = findings[12]
            self.assertEqual("WAF Detection", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.references)
            self.assertIsNone(finding.unsaved_tags)
            self.assertEqual(None, finding.unsaved_endpoints[0].path)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(443, finding.unsaved_endpoints[0].port)
            self.assertEqual("waf-detect", finding.vuln_id_from_tool)

        with self.subTest(i=14):
            finding = findings[14]
            self.assertEqual("phpMyAdmin Panel", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.references)
            self.assertIn("panel", finding.unsaved_tags)
            self.assertEqual("phpmyadmin/", finding.unsaved_endpoints[0].path)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(443, finding.unsaved_endpoints[0].port)
            self.assertEqual("phpmyadmin-panel", finding.vuln_id_from_tool)

        with self.subTest(i=15):
            finding = findings[15]
            self.assertEqual("MySQL DB with enabled native password", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIsNone(finding.references)
            self.assertIn("network", finding.unsaved_tags)
            self.assertIn("mysql", finding.unsaved_tags)
            self.assertIn("bruteforce", finding.unsaved_tags)
            self.assertIn("db", finding.unsaved_tags)
            self.assertEqual(None, finding.unsaved_endpoints[0].path)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(3306, finding.unsaved_endpoints[0].port)
            self.assertEqual("mysql-native-password-bruteforce", finding.vuln_id_from_tool)

    def test_parse_many_findings_new(self):
        testfile = open("unittests/scans/nuclei/many_findings_new.json")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()

        self.assertEqual(2, len(findings))
        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("OpenSSH Username Enumeration v7.7", finding.title)
            self.assertEqual("Medium", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertIsNotNone(finding.description)
            self.assertIn("network", finding.unsaved_tags)
            self.assertIn("openssh", finding.unsaved_tags)
            self.assertIn("cve", finding.unsaved_tags)
            self.assertIsNotNone(finding.references)
            self.assertEqual("nuclei-example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(22, finding.unsaved_endpoints[0].port)
            self.assertEqual("CVE-2018-15473", finding.vuln_id_from_tool)
            vulnerability_ids = finding.unsaved_vulnerability_ids
            self.assertEqual(1, len(vulnerability_ids))
            self.assertIn('CVE-2018-15473', vulnerability_ids)
            self.assertEqual(362, finding.cwe)
            self.assertEqual("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N", finding.cvssv3)
            self.assertEqual(5.3, finding.cvssv3_score)

        with self.subTest(i=1):
            finding = findings[1]
            self.assertEqual("Exposed Prometheus metrics", finding.title)
            self.assertEqual("Low", finding.severity)
            self.assertEqual(1, finding.nb_occurences)
            self.assertEqual('', finding.description)
            self.assertIn("config", finding.unsaved_tags)
            self.assertIn("exposure", finding.unsaved_tags)
            self.assertIn("prometheus", finding.unsaved_tags)
            self.assertIsNotNone(finding.references)
            self.assertEqual("prometheus-metrics", finding.vuln_id_from_tool)

    def test_parse_many_findings_third(self):
        testfile = open("unittests/scans/nuclei/many_findings_third.json")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()

        self.assertEqual(2, len(findings))
        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("HTTP Missing Security Headers", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertIsNotNone(finding.unsaved_request)
            self.assertIsNotNone(finding.unsaved_response)
            self.assertIsNotNone(finding.steps_to_reproduce)
            self.assertEqual(3, len(finding.unsaved_tags))
            self.assertEqual("example.com", finding.unsaved_endpoints[0].host)
            self.assertEqual(443, finding.unsaved_endpoints[0].port)
            self.assertEqual("http-missing-security-headers", finding.vuln_id_from_tool)
            self.assertEqual("x-content-type-options", finding.component_name)
            self.assertEqual(finding.date,
                datetime(2023, 3, 13, 11, 2, 11, 829446, tzinfo=tzoffset(None, 10800)))

        with self.subTest(i=1):
            finding = findings[1]
            self.assertEqual("favicon-detection", finding.title)
            self.assertEqual("Info", finding.severity)
            self.assertIsNotNone(finding.steps_to_reproduce)
            self.assertEqual(4, finding.references.count("\n"))
            self.assertEqual("favicon-detect", finding.vuln_id_from_tool)
            self.assertEqual("asp.net-favicon", finding.component_name)

    def test_parse_many_findings_v3(self):
        testfile = open("unittests/scans/nuclei/multiple_v3.json")
        parser = NucleiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(5, len(findings))
        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("Info", finding.severity)

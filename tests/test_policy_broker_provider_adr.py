from pathlib import Path
import unittest


ADR = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "adr"
    / "0001-policy-broker-signing-provider.md"
).read_text()


class PolicyBrokerProviderAdrTest(unittest.TestCase):
    def test_fixes_sign_only_provider_and_algorithm(self) -> None:
        self.assertIn("Status: Accepted", ADR)
        self.assertIn("AWS KMS", ADR)
        self.assertIn("AWS Lambda", ADR)
        self.assertIn("RSASSA_PKCS1_V1_5_SHA_256", ADR)
        self.assertIn("PKCS#8 DER", ADR)
        self.assertIn("`kms:Sign`", ADR)

    def test_keeps_credentials_out_of_local_and_ci_runtimes(self) -> None:
        for forbidden_runtime in [
            "local Mac",
            "GitHub Actions",
            "Doppler",
            "self-hosted runner",
            "AIris VibeOS",
        ]:
            self.assertIn(forbidden_runtime, ADR)
        self.assertIn("long-lived AWS access keyは発行しない", ADR)
        self.assertIn("local tokenへのfallbackは設けない", ADR)

    def test_fixes_non_weakening_mutation_and_provisioning_stop(self) -> None:
        self.assertIn("ruleset ID: `19456040`", ADR)
        self.assertIn("SHA 1値だけ", ADR)
        self.assertIn("kill switchは既定deny", ADR)
        self.assertIn("AWS account ID、region、billing owner", ADR)
        self.assertIn("production provisioningの明示的前提条件", ADR)


if __name__ == "__main__":
    unittest.main()

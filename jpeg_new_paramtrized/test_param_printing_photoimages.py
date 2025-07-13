import logging
import pytest
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def teardown_method(self):
        """Clean up resources after each test."""
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()
        self.job_history.clear()
        self.job_history.wait_for_history_empty()
        self.media.update_media_configuration(self.default_configuration)

    @pytest.mark.parametrize(
        "job_hash, log_message",
        [
            (
                "34d2105b65aaea33b7ab03e50e51f9a756f6d160514c26903c4595054d0efa62",
                "Jpeg file example photoimages 1PhotoDPOFTestforBAT hp945 Vader DCIM 100HP945 HPIM0071 - Print job completed successfully",
            ),
            (
                "8f2683c349abb62cf15b5eb799d9c35d05ed45db7f3ba6863629421275921d65",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 1 - Print job completed successfully",
            ),
            (
                "27e760e042664eccb2b50c1fad3417297544641071d6d012b86c2f32a8d89bf1",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 101 - Print job completed successfully",
            ),
            (
                "fdb091a4bccb830fdb1421688f74e708827434b6d7e1c6cde9db12b39c1b957b",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 102 - Print job completed successfully",
            ),
            (
                "f98149047349fc2c16b7702ddf9f624a6094f335ad113a699e3dd88bc85c41f8",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 104 - Print job completed successfully",
            ),
            (
                "d4adbb615180a94df9fc92a517ab55609eb0a7b824e93b073b210104916e45dd",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 108 - Print job completed successfully",
            ),
            (
                "3a1ec20759147990cf9862dd43a464d15a3628abdd57e3b6d585996c8c38e56b",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 21 - Print job completed successfully",
            ),
            (
                "8a479ef7128345004b50b10056901496642e199ec29d434c5fa7cb6cffc42b57",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 22 - Print job completed successfully",
            ),
            (
                "d543b80d11d21075192efdf9b01f9987faa0cb6a57721f10b54bd8c04f1df39a",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 24 - Print job completed successfully",
            ),
            (
                "81fc17818224be0036736ce53e5804c5695fe1a4606c96fe694f4b0034c510da",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 26 - Print job completed successfully",
            ),
            (
                "65c6e47b8a16cc8134fe3cdf42a2f43a8fc187a5816afec15982746e3e257210",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 45 - Print job completed successfully",
            ),
            (
                "143829ed3af12fe47429e199b4d725b6bb4e1ce44138debc6e5c2e06899d0393",
                "Jpeg file example photoimages 300 2000 Quality Test Photos 50 - Print job completed successfully",
            ),
            (
                "1497ed339f914418a8fb1329a1117c3668266884fbef99901ec6dcfaa73631de",
                "Jpeg file example photoimages Redeyeimages 250Nonredeye IMG 6487 - Print job completed successfully",
            ),
            (
                "427585da86657e376a639a6259002ef94d72006de5c4caa897f60a1de3ddfe84",
                "Jpeg file example photoimages smalljpg imge26 medium - Print job completed successfully",
            ),
            (
                "a68759e088816aa1e0e8764b335a68d0a3fad4dea4db09e7c6456826b6fd09b9",
                "Jpeg photoimages AutoAlign Portrait 3x4 IMG 0322 file",
            ),
            (
                "e3e510bc084382297091821906875e620bc5bb1aa6f520e8b40ca86c699eb2e2",
                "Jpeg photoimages_panoramaimages_HPR927_5M_3 file",
            ),
        ],
    )
    def test_when_photoimages_then_succeeds(self, job_hash, log_message):
        job_id = self.print.raw.start(job_hash)
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info(log_message)

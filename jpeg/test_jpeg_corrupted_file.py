import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple Print job of Jpeg file of 1MB from **
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:DatastreamCorrupted.JPG=8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122
    +test_classification:System
    +name:test_jpeg_corrupted_file
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_corrupted_file
        +guid:74b93202-6794-11eb-8168-bba14bd06d0a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_corrupted_file(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8569b17b86977b3f02e3c5194d6436df02662bc5724f929f007a1a4626a9f122', expected_job_state='FAILED')
    outputsaver.save_output()
    outputsaver.clear_output()
    logging.info("Jpeg corrupted file")

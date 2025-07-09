import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg Performance faces Page from *faces.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:faces.jpg=d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2
    +test_classification:System
    +name:test_jpeg_performance_faces
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_performance_faces
        +guid:32b7a848-03cf-424f-aefb-5dbc0cbedbd7
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
    +overrides:
        +Home:
            +is_manual:False
            +timeout:240
            +test:
                +dut:
                    +type:Engine

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_performance_faces(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2')
    outputsaver.save_output()

    logging.info("JPEG Performance faces Page - Print job completed successfully")

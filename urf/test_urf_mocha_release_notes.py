import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Mocha Release Notes Page from *MochaReleaseNotes.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:MochaReleaseNotes.urf=4f58e92c69b089c787efe90ed9a9bec69a58e90d3a128c4b0ca9d1e1dd4208de
    +name:test_urf_mocha_release_notes_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_mocha_release_notes_page
        +guid:c8cea316-0c4c-4045-aa3b-b6375d7fa922
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_mocha_release_notes_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: In case of failure in the future, check for media size requested, load if supported
    printjob.print_verify('4f58e92c69b089c787efe90ed9a9bec69a58e90d3a128c4b0ca9d1e1dd4208de')
    outputsaver.save_output()

    logging.info("URF Mocha Release Notes Page - Print job completed successfully")

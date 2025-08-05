import pytest
import logging

from dunetuf.network.ipp.ipp_utils import update_ipp_datfile
from dunetuf.print.output.intents import Intents

PRINT_URF_FLIPPED_JOB_TEST_FILE_PATH = "/code/tests/print/pdl/ipp/attributes/10x12_URF.test"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using flipped job media size
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-209592
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10x12_URF.urf=7ec7f6d299a44e3c52dc224c02826eb2a0afb7d09ef4942635962c69d8f9cbf5
    +name:test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize
        +guid:31b90aa3-5466-4a30-b821-72d13f4770d7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=ROLL2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize(setup_teardown, printjob, outputverifier, tray):

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_URF_FLIPPED_JOB_TEST_FILE_PATH)

    printjob.ipp_print(update_dat_file, '7ec7f6d299a44e3c52dc224c02826eb2a0afb7d09ef4942635962c69d8f9cbf5')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_page_width(Intents.printintent, 7200)
    outputverifier.verify_page_height(Intents.printintent, 6000)

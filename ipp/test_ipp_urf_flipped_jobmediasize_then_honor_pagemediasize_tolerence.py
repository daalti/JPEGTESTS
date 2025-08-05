import pytest
import logging

from dunetuf.network.ipp.ipp_utils import update_ipp_datfile
from dunetuf.print.output.intents import Intents

PRINT_URF_FLIPPED_JOB__TOLERENCE_TEST_FILE_PATH = "/code/tests/print/pdl/ipp/attributes/A4_URF.test"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using flipped job media size with tolerance
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-209592
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_URF.urf=d7c1229896b644238441c09a6c60a83b92aadbf4edbea98ad7c0e2a435b8af80
    +name:test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize_tolerence
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize_tolerence
        +guid:c4cc747f-df2a-4446-bdb8-6d9c52078fb7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=ROLL2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_flipped_jobmediasize_then_honor_pagemediasize_tolerence(setup_teardown, printjob, outputverifier, tray):

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_URF_FLIPPED_JOB__TOLERENCE_TEST_FILE_PATH)

    printjob.ipp_print(update_dat_file, 'd7c1229896b644238441c09a6c60a83b92aadbf4edbea98ad7c0e2a435b8af80')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_page_width(Intents.printintent, 7016)
    outputverifier.verify_page_height(Intents.printintent, 4961)

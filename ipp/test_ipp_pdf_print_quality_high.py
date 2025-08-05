import pytest

from dunetuf.print.output.intents import Intents, PrintQuality
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value print_quality_high
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_ipp_pdf_print_quality_high
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pdf_print_quality_high
        +guid:75064f7f-d2c6-448d-b6fc-811b34d421a3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pdf_print_quality_high(setup_teardown, printjob, outputverifier, outputsaver, configuration):
    outputsaver.operation_mode('TIFF')
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    print_quality_high = 5
    ipp_test_attribs = {'document-format': 'application/pdf', 'print-quality': print_quality_high}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, count=5)
    
    if configuration.productname == "jupiter":
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.best) # Jupiter does not support maximum quality with plain paper so it will print with best quality
    else:
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
    outputsaver.operation_mode('NONE')

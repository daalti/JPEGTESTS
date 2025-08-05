import pytest
import logging
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
from dunetuf.print.output.intents import Intents, PrintQuality, MediaType, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value print-quality_economode.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-239639
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_pdl_intent_ipp_jpg_print_quality_economode
    +test:
        +title:test_pdl_intent_ipp_jpg_print_quality_economode
        +guid:8837d23d-b633-416f-81b0-419b11a55969
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in & Print=Economode & PrintEngineType=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_jpg_print_quality_economode(printjob, outputsaver, tray, outputverifier):
    job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
    ipp_test_attribs = {'document-format': 'image/jpeg', 'print-quality': 3, 'media-type': 'stationery', 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputsaver.save_output()
    outputverifier.save_and_parse_output()

    outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[3]])
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    tray.reset_trays()
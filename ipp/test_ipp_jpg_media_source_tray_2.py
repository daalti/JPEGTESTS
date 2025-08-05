import pytest

from dunetuf.print.output.intents import Intents, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file using attribute value media_source_tray_2
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
    +test_classification:System
    +name:test_ipp_jpg_media_source_tray_2
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpg_media_source_tray_2
        +guid:e30a26a3-0277-44d9-995e-59bafa3f7186
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpg_media_source_tray_2(setup_teardown, printjob, outputverifier, tray):
    trays = tray.get_tray_configuration()
    tray2 = trays[1]["mediaSourceId"]
    if tray.is_size_supported('iso_a4_210x297mm', tray2):
        tray.configure_tray(tray2, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media-source': tray2, 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
    outputverifier.save_and_parse_output()
    tray2 = "tray2" if tray2 == "tray-2" else tray2
    outputverifier.verify_media_source(Intents.printintent, getattr(MediaSource,f"{tray2}"))
    tray.reset_trays()

import pytest
from dunetuf.print.output.intents import Intents, MediaSource


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-source_tray-1
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_600.urf=6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f
    +name:test_ipp_urf_media_source_tray_1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_media_source_tray_1
        +guid:c5625cba-e85c-42f8-a38e-3f77a12890f7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_media_source_tray_1(setup_teardown, printjob, outputverifier, tray):
    trays = tray.get_tray_configuration()
    tray1 = trays[0]["mediaSourceId"]
    if tray.is_size_supported('iso_a4_210x297mm', tray1):
        tray.configure_tray(tray1, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/urf', 'media-source': tray1, 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '6f574dcc72506c503075530d8e6a9695a466657ddb552ccc4afbab95c54b4c0f')
    outputverifier.save_and_parse_output()
    tray1 = "tray1" if tray1 == "tray-1" else tray1
    outputverifier.verify_media_source(Intents.printintent, getattr(MediaSource,f"{tray1}"))
    tray.reset_trays()

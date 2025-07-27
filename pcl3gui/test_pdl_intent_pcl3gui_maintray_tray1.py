import pytest
from dunetuf.print.output.intents import Intents, MediaSource

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Pcl3gui and ensure the PDL setting the tray which is installed in the printer
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-145007
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter-Plain-Marconi_Hi-tray_1.prn=78f135c0c44424edd57be3c4f5758f628893c7400eab009686f1e7c32268769a
    +name:test_pdl_intent_pcl3gui_maintray_tray1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_pcl3gui_maintray_tray1
        +guid:a26f33b0-dd62-4531-92cd-ad686ab1831d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_pcl3gui_maintray_tray1(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):

    printjob.print_verify('78f135c0c44424edd57be3c4f5758f628893c7400eab009686f1e7c32268769a')
    outputverifier.save_and_parse_output()

    if tray.is_tray_supported('main'):
        outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
    elif tray.is_tray_supported('tray-1'):
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    elif tray.is_tray_supported('main-roll'):
        outputverifier.verify_media_source(Intents.printintent, MediaSource.mainRoll)
    elif tray.is_tray_supported('roll-1'):
        outputverifier.verify_media_source(Intents.printintent, MediaSource.roll1)
    else :
        assert(0)
    #!!! Or avoid running in jupiter if this is only for tray
    tray.reset_trays()
    outputsaver.save_output()

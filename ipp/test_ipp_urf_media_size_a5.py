import pytest
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-size_a5
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
    +name:test_ipp_urf_media_size_a5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_media_size_a5
        +guid:06e77391-a2b2-4efa-a276-9b0bff8b0c0c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & MediaSizeSupported=iso_a5_148x210mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_media_size_a5(setup_teardown, printjob, outputsaver, tray, print_emulation):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
            print_emulation.tray.setup_tray(
                trayid="all",
                media_size=MediaSize.A5.name,
                media_type=MediaType.Plain.name,
                orientation=MediaOrientation.Default.name,
                level=TrayLevel.Full.name
            )
    elif tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/urf', 'media': 'iso_a5_148x210mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

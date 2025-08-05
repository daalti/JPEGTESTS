import pytest
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a URF file using attribute value media-size_a4
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
    +name:test_ipp_urf_media_size_a4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_urf_media_size_a4
        +guid:274dbe0a-8666-4433-88b1-80568aa7f294
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_urf_media_size_a4(setup_teardown, print_emulation, configuration,printjob, outputsaver, tray):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
            tray1 = MediaInputIds.Tray1.name
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, MediaSize.A4.name, MediaType.Plain.name)
            print_emulation.tray.close(tray1)
        else:
            tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    ipp_test_attribs = {'document-format': 'image/urf', 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()

import pytest
from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, ColorMode, PrintQuality, Plex, PlexBinding, MediaType, ContentOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a Email from Mac and using attribute value media size A4
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-124180
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:mac_mail.bin=087b82a070ac66ca8cc81aa1f7fc3d7baec41e47a160d58f07232839616dd22f
    +test_classification:System
    +name:test_pdl_airprint_mac_mail_mediasize_A4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_airprint_mac_mail_mediasize_A4
        +guid:57c6541b-de83-458e-a824-3381b944cc53
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & Print=Normal & Duplexer=True & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_airprint_mac_mail_mediasize_A4(setup_teardown, printjob, outputsaver, tray, outputverifier, cdm):
    outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    if cdm.device_feature_cdm.is_color_supported():
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'iso_a4_210x297mm', 'print-color-mode': 'color', 'print-quality': 4, 'sides': 'two-sided-long-edge', 'copies':2, 'media-type': 'stationery', 'orientation-requested': 3, 'media-source': 'tray-1'}
    else:
        ipp_test_attribs = {'document-format': 'application/pdf', 'media': 'iso_a4_210x297mm', 'print-color-mode': 'monochrome', 'print-quality': 4, 'sides': 'two-sided-long-edge', 'copies':2, 'media-type': 'stationery', 'orientation-requested': 3, 'media-source': 'tray-1'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '087b82a070ac66ca8cc81aa1f7fc3d7baec41e47a160d58f07232839616dd22f')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 4)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 2)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
    if cdm.device_feature_cdm.is_color_supported():
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
    else:
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.monochrome)
    outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
    outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    tray.reset_trays()
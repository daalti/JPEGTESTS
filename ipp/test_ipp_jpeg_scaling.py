import pytest
from dunetuf.print.output.intents import Intents, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file without Mediasize sent by user
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-126155
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_4x6.prn=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_ipp_jpeg_scaling
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpeg_scaling
        +guid:490536f1-56af-47d2-ab7c-ab162b0f3f51
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_letter_8.5x11in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpeg_scaling(setup_teardown, printjob, outputverifier, tray):
    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'na_letter_8.5x11in' }
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        expected_media_size = MediaSize.letter
    

    printjob.ipp_print(ipp_test_file, 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1',timeout = 300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file with Mediasize and auto Mediasource sent by user
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-126155
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_4x6.prn=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_ipp_jpeg_Mediasize_and_Mediasource_sent
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpeg_Mediasize_and_Mediasource_sent
        +guid:e32457d3-f7cc-4bdc-b8ef-a1b3beac1130
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpeg_Mediasize_and_Mediasource_sent(setup_teardown, printjob, outputverifier, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        expected_media_size = MediaSize.letter

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media-source': 'auto', 'media': 'iso_a4_210x297mm'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)


    printjob.ipp_print(ipp_test_file, 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1',timeout = 300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file with Mediasize sent by user nad is loaded in source
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-126155
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_4x6.prn=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_ipp_jpeg_Mediasize_sent
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpeg_Mediasize_sent
        +guid:1a4b890e-feda-4b41-aab7-05fae6b289c8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpeg_Mediasize_sent(setup_teardown, printjob, outputverifier, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        expected_media_size = MediaSize.letter

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)


    printjob.ipp_print(ipp_test_file, 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1',timeout = 300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a JPG file with Mediasize sent by user and is not loaded in any tray
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-126155
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_4x6.prn=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_ipp_jpeg_Mediasize_sent_not_loaded
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_jpeg_Mediasize_sent_not_loaded
        +guid:3b1756af-dfdb-4688-8b9b-b9e2bc8193b4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_jpeg_Mediasize_sent_not_loaded(setup_teardown, printjob, outputverifier, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        expected_media_size = MediaSize.letter

    ipp_test_attribs = {'document-format': 'image/jpeg', 'media': 'na_index-4x6_4x6in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)


    printjob.ipp_print(ipp_test_file, 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1',timeout = 300)
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    tray.reset_trays()

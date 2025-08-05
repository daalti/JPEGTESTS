from dunetuf.network.ipp.ipp_utils import update_ipp_datfile
from dunetuf.print.output.intents import Intents, MediaSize
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaType as PrintMediaType, MediaOrientation

PRINT_MEDIA_SIZE_TEST_FILE_PATH = "/code/tests/print/pdl/ipp/attributes/print_media_size.test"
PRINT_PWG_TEST_FILE_PATH = "/code/tests/print/pdl/ipp/attributes/print_pwg.test"
LETTER_WIDTH_IN_INCH = 8.5
LETTER_HEIGHT_IN_INCH = 11.0
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page letter sgray 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-letter-sgray-8-300dpi.pwg=c1e5b49ce2c26854bae86cb347e19eaa8a722db01d49fe57f90c5b38787cd3ef
    +test_classification:System
    +name:test_ipp_pwg_1page_letter_sgray_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_letter_sgray_8_300dpi
        +guid:9a04f9ea-717b-4f03-9a37-c0040bc8ac8f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_letter_sgray_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, cdm, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='27940')

    printjob.ipp_print(update_dat_file, 'c1e5b49ce2c26854bae86cb347e19eaa8a722db01d49fe57f90c5b38787cd3ef')
    outputverifier.save_and_parse_output()

    default_source = tray.get_default_source()
    expected_media_size = MediaSize.letter
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(8.5 * job_resolution)
        expected_height = round(11 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 srgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-srgb-8-600dpi.pwg=3a2ff2f6f97b53530570527ea67057c656660d4ecdb59bcc2e7c75537a22697b
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_srgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_srgb_8_600dpi
        +guid:5d26e265-88ad-463d-bbc5-df8429dfe724
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_srgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '3a2ff2f6f97b53530570527ea67057c656660d4ecdb59bcc2e7c75537a22697b')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page a4 srgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-a4-srgb-8-600dpi.pwg=53b98092d75a6b74ec185227e332f0fd99c64c69ae7e039cd861e99732eb4e16
    +test_classification:System
    +name:test_ipp_pwg_1page_a4_srgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_a4_srgb_8_600dpi
        +guid:e4a67c9f-4a97-4a75-94cd-7c3bca9fcb9a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_a4_srgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, '53b98092d75a6b74ec185227e332f0fd99c64c69ae7e039cd861e99732eb4e16')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page letter srgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-600dpi.pwg=d4216f40efeb76eefffd6784d074c5ce7cbc6a2a5ee32345c8c55eb224d65dfe
    +test_classification:System
    +name:test_ipp_pwg_1page_letter_srgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_letter_srgb_8_600dpi
        +guid:a03b8ba1-10e2-4ff1-8b65-70f49520aba9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_letter_srgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, cdm, udw) :
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='27940')

    printjob.ipp_print(update_dat_file, 'd4216f40efeb76eefffd6784d074c5ce7cbc6a2a5ee32345c8c55eb224d65dfe')
    outputverifier.save_and_parse_output()
    default_source = tray.get_default_source()
    expected_media_size = MediaSize.letter
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(8.5 * job_resolution)
        expected_height = round(11 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 srgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-srgb-16-600dpi.pwg=8a4dbe4f0cbe09bc8482e98e9aa446d2b9caddf9afa78ac0bcc903bd5ee0c3c9
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_srgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_srgb_16_600dpi
        +guid:41262f5b-0ffb-41cf-85ba-c37487190957
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_ipp_pwg_color_jpg_4x6_srgb_16_600dpi(setup_teardown, printjob, outputverifier, tray):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '8a4dbe4f0cbe09bc8482e98e9aa446d2b9caddf9afa78ac0bcc903bd5ee0c3c9', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 adobe rgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-adobe-rgb-8-600dpi.pwg=ef6d44eee24cb156f1ca3ceb269fafccb3b53a34d0eabf38023c499d33a0ec59
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_600dpi
        +guid:e33aa52f-0000-4ef2-8a62-01f8db899a06
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, 'ef6d44eee24cb156f1ca3ceb269fafccb3b53a34d0eabf38023c499d33a0ec59')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177684 ipp test for color jpg 4x6 adobe rgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-adobe-srgb-16-600dpi.pwg=693355b1123839cd81b0f6721eb5121419365374a83b3bbe304ed5a24e0e17fc
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_600dpi
        +guid:b73ecbb3-895e-4156-8ecc-5d13114765dc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_600dpi(setup_teardown, printjob, outputverifier, tray, reset_tray):
    logging.info("For failed print job, CRC is null. No need to check CRC for this case.")
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '693355b1123839cd81b0f6721eb5121419365374a83b3bbe304ed5a24e0e17fc', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for pwg color jpg 4x6 sgray 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-sgray-8-600dpi.pwg=70c654fbd3e97b1fcf16d5a60dc4a46ec5d497780af35edbb2ba19d3bacc17f0
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_sgray_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_sgray_8_600dpi
        +guid:e9da6deb-4cea-420d-b3f4-00572ed23140
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_sgray_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '70c654fbd3e97b1fcf16d5a60dc4a46ec5d497780af35edbb2ba19d3bacc17f0')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page a4 sgray 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-a4-sgray-8-600dpi.pwg=e7f3f3fa0c328754e870e6b33ce4e396eeeacf4a176c6c1925ec4e7e04dfc2e6
    +test_classification:System
    +name:test_ipp_pwg_1page_a4_sgray_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_a4_sgray_8_600dpi
        +guid:1efcda99-2f5b-4ed6-b525-c47c679c850b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_a4_sgray_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, 'e7f3f3fa0c328754e870e6b33ce4e396eeeacf4a176c6c1925ec4e7e04dfc2e6')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page letter sgray 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-letter-sgray-8-600dpi.pwg=df51655e8f48eead0b875dd30e532ef5f6badacd2caab8b875cd9b2fc3ad1957
    +test_classification:System
    +name:test_ipp_pwg_1page_letter_sgray_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_letter_sgray_8_600dpi
        +guid:02333a90-fac7-4d9f-a55a-ce4a084b71f6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_letter_sgray_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, cdm, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='27940')

    printjob.ipp_print(update_dat_file, 'df51655e8f48eead0b875dd30e532ef5f6badacd2caab8b875cd9b2fc3ad1957')
    outputverifier.save_and_parse_output()

    default_source = tray.get_default_source()
    expected_media_size = MediaSize.letter
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(8.5 * job_resolution)
        expected_height = round(11 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 srgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-srgb-8-300dpi.pwg=fe6cf0dc2aae41dbaef47e7fd0da6ee4140756f604ee4f4cb116a4630ba8866b
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_srgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_srgb_8_300dpi
        +guid:890b5873-95ad-4dcb-9f5c-52832e22bbde
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_srgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, 'fe6cf0dc2aae41dbaef47e7fd0da6ee4140756f604ee4f4cb116a4630ba8866b')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page a4 srgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-a4-srgb-8-300dpi.pwg=04b99fad4c8b6af13d48a32bae96f129e564def61a5733b0072f48527829ad57
    +test_classification:System
    +name:test_ipp_pwg_1page_a4_srgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_a4_srgb_8_300dpi
        +guid:4da11dc8-e48e-4655-8498-e51937e373fe
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_a4_srgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, '04b99fad4c8b6af13d48a32bae96f129e564def61a5733b0072f48527829ad57')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 srgb 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-srgb-16-300dpi.pwg=fb5c7eb5dbdf0ef533a28d31e073dcc6b36059eff34f5b8460f0c2760d549ddf
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_srgb_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_srgb_16_300dpi
        +guid:f6871a45-139e-4e2e-a85f-3438d911e56e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_srgb_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, 'fb5c7eb5dbdf0ef533a28d31e073dcc6b36059eff34f5b8460f0c2760d549ddf', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177685 ipp test for color jpg 4x6 adobe rgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-adobe-srgb-8-300dpi.pwg=1d55c569b7402503dafc1521d4d5aec3c0f239d06b7ab351fbbfc7ab6aabc0d6
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_300dpi
        +guid:5303f4d2-5a44-4ee0-9004-0a6b36ed570d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_adobe_rgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw, reset_tray):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '1d55c569b7402503dafc1521d4d5aec3c0f239d06b7ab351fbbfc7ab6aabc0d6')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177686 ipp test for color jpg 4x6 adobe rgb 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-adobe-srgb-16-300dpi.pwg=84e8334a2a2c370ffe7a8ecb930ff229aa2ad883e537c6d0379dd98db8c7851d
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_300dpi
        +guid:a18efe63-49e5-4b07-927c-3a89a0177a7e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_adobe_rgb_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, reset_tray):
    logging.info("For failed print job, CRC is null. No need to check CRC for this case.")
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '84e8334a2a2c370ffe7a8ecb930ff229aa2ad883e537c6d0379dd98db8c7851d', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for color jpg 4x6 sgray 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:color.jpg-4x6-sgray-8-300dpi.pwg=d6ad2b81a8d05c9655d536a9fc17826dc9376755659a33dc068faf52404a0e5e
    +test_classification:System
    +name:test_ipp_pwg_color_jpg_4x6_sgray_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_color_jpg_4x6_sgray_8_300dpi
        +guid:18c07fc2-64d0-45a4-8c37-a76d2f0ff94a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_color_jpg_4x6_sgray_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, 'd6ad2b81a8d05c9655d536a9fc17826dc9376755659a33dc068faf52404a0e5e')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 1page a4 sgray 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-a4-sgray-8-300dpi.pwg=31557199b4b912d44952801024ef3bb09bcac13ce8ac055d20d22dd155ca35e1
    +test_classification:System
    +name:test_ipp_pwg_1page_a4_sgray_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_1page_a4_sgray_8_300dpi
        +guid:e01379a1-e6b3-41f8-a12d-309bdc28342e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_1page_a4_sgray_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_PWG_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, '31557199b4b912d44952801024ef3bb09bcac13ce8ac055d20d22dd155ca35e1')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177688 ipp test for a4 sgray 8 600dpi pwg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4-sgray-8-600dpi.pwg=b50d39b6eb0261d533b8881bcaa48d243d8353ec827178f8792bb100bb7daf38
    +test_classification:System
    +name:test_ipp_pwg_a4_sgray_8_600dpi_pwg
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_a4_sgray_8_600dpi_pwg
        +guid:25fe37dc-9c8c-4712-9319-d814129661a8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_a4_sgray_8_600dpi_pwg(setup_teardown, printjob, outputverifier, tray, outputsaver, udw, reset_tray, print_emulation,configuration,):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()

        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)
            if "A4" in supported_sizes and "Plain" in supported_types:
                print_emulation.tray.open(tray_id)
                print_emulation.tray.load(tray_id, "A4", "Plain",
                                          media_orientation=MediaOrientation.Portrait.name)
                expected_media_size = MediaSize.a4
                print_emulation.tray.close(tray_id)
                break
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, 'b50d39b6eb0261d533b8881bcaa48d243d8353ec827178f8792bb100bb7daf38')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for a5 sgray 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A5-sgray-16-300dpi.pwg=c7e9f55a318c9159aa406c6b54b78d4667f8a40cd493ac95dbf723fbb3cfe413
    +test_classification:System
    +name:test_ipp_pwg_a5_sgray_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_a5_sgray_16_300dpi
        +guid:3c392825-5b3d-4280-ad79-bc591d95cc25
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_a5_sgray_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a5_148x210mm', default):
        tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')
        expected_media_size = MediaSize.a5
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='14800', tempvalue2='ydim', value2='21000')

    printjob.ipp_print(update_dat_file, 'c7e9f55a318c9159aa406c6b54b78d4667f8a40cd493ac95dbf723fbb3cfe413', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for a6 sgray 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A6-sgray-16-300dpi.pwg=04c1f15d57871b330283387b51f187a5f2e7a0a3b43a85a9d0b542d648103ff1
    +test_classification:System
    +name:test_ipp_pwg_a6_sgray_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_a6_sgray_16_300dpi
        +guid:9c80e750-be56-4abc-995f-67f04b5be01b
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=iso_a6_105x148mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_a6_sgray_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a6_105x148mm', default):
        tray.configure_tray(default, 'iso_a6_105x148mm', 'stationery')
        expected_media_size = MediaSize.a6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10500', tempvalue2='ydim', value2='14800')

    printjob.ipp_print(update_dat_file, '04c1f15d57871b330283387b51f187a5f2e7a0a3b43a85a9d0b542d648103ff1')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for b5 sgray 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5-sgray-16-600dpi.pwg=aa9203fdf466bee7395f9a84b8e2f8d612d9293aeb7aae6497e267ec3138dd09
    +test_classification:System
    +name:test_ipp_pwg_b5_sgray_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_b5_sgray_16_600dpi
        +guid:71416758-a506-4316-b3a0-9f1a8e10d979
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_b5_sgray_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')
        expected_media_size = MediaSize.b5envelope
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='17600', tempvalue2='ydim', value2='25000')

    printjob.ipp_print(update_dat_file, 'aa9203fdf466bee7395f9a84b8e2f8d612d9293aeb7aae6497e267ec3138dd09')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for  envelope 10 sgray 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-10-sgray-16-600dpi.pwg=022ddf1d0f9815ee1da1b5941aa55e32a80b4f1cbfaed8c07c35566e00bd9c59
    +test_classification:System
    +name:test_ipp_pwg_envelope_10_sgray_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_10_sgray_16_600dpi
        +guid:52a5c1df-ca44-4e28-8c3f-03f22aa5c793
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_10_sgray_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')
        expected_media_size = MediaSize.com10envelope
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10477', tempvalue2='ydim', value2='24130')

    printjob.ipp_print(update_dat_file, '022ddf1d0f9815ee1da1b5941aa55e32a80b4f1cbfaed8c07c35566e00bd9c59')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for envelope c5 adobe rgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-C5-adobe-rgb-8-300dpi.pwg=9641637155c5e57dad1b287dce45bc04abedc6651fc53c983aff29ef0555a621
    +test_classification:System
    +name:test_ipp_pwg_envelope_c5_adobe_rgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_c5_adobe_rgb_8_300dpi
        +guid:45ff7328-7c76-4f01-9a8c-555185516a4c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=iso_c5_162x229mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_c5_adobe_rgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_c5_162x229mm', default):
        tray.configure_tray(default, 'iso_c5_162x229mm', 'stationery')
        expected_media_size = MediaSize.c5envelope
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='16200', tempvalue2='ydim', value2='22900')

    printjob.ipp_print(update_dat_file, '9641637155c5e57dad1b287dce45bc04abedc6651fc53c983aff29ef0555a621')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for envelope c6 adobe rgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-C6-adobe-rgb-8-300dpi.pwg=2d8c51a0a2c5f3ef0c5c18158dbcf19095e77516472a65717a9aba184efb36ce
    +test_classification:System
    +name:test_ipp_pwg_envelope_c6_adobe_rgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_c6_adobe_rgb_8_300dpi
        +guid:c635c537-0798-4f69-9acf-1b9ad11c3bb0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=iso_c6_114x162mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_c6_adobe_rgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_c6_114x162mm', default):
        tray.configure_tray(default, 'iso_c6_114x162mm', 'stationery')
        expected_media_size = MediaSize.c6envelope
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='11400', tempvalue2='ydim', value2='16200')

    printjob.ipp_print(update_dat_file, '2d8c51a0a2c5f3ef0c5c18158dbcf19095e77516472a65717a9aba184efb36ce',timeout=200)
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test ipp pwg envelope chou 3 srgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-Chou-3-srgb-16-600dpi.pwg=bb2c5df5fbb90b3e2bee616cd3c397f37cb39978bd37417248e4c4e3eb510460
    +test_classification:System
    +name:test_ipp_pwg_envelope_chou_3_srgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_chou_3_srgb_16_600dpi
        +guid:89e37be5-1a52-4e1d-b5cd-c586587e6516
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=jpn_chou3_120x235mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_chou_3_srgb_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('jpn_chou3_120x235mm', default):
        tray.configure_tray(default, 'jpn_chou3_120x235mm', 'stationery')
        expected_media_size = MediaSize.chou3_envelope
    elif tray.is_size_supported('custom', default):
        # TODO: Beam defaults unsupported media sizes to A4 whereas Ulysses and
        #  Selene defaults Letter. In the absence of firmware interface to check
        # the default media size, this block works as a workaround - as Beam
        # does not support Custom sizes on multi-sheet tray.
        pass
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='12000', tempvalue2='ydim', value2='23500')

    printjob.ipp_print(update_dat_file, 'bb2c5df5fbb90b3e2bee616cd3c397f37cb39978bd37417248e4c4e3eb510460')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for envelope chou4 srgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-Chou4-srgb-16-600dpi.pwg=6e778acc2cca3fad4be32b35b52d816c17875305ba02cb01b8bcebd7329a27a0
    +test_classification:System
    +name:test_ipp_pwg_envelope_chou4_srgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_chou4_srgb_16_600dpi
        +guid:5264b8ad-8c35-4216-b146-c3fcc5cc3fd5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=jpn_chou4_90x205mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_chou4_srgb_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()

    if tray.is_size_supported('jpn_chou4_90x205mm', default):
        tray.configure_tray(default, 'jpn_chou4_90x205mm', 'stationery')
        expected_media_size = MediaSize.chou4_envelope
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='9000', tempvalue2='ydim', value2='20500')

    printjob.ipp_print(update_dat_file, '6e778acc2cca3fad4be32b35b52d816c17875305ba02cb01b8bcebd7329a27a0')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for envelope dl sgray 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-DL-sgray-16-600dpi.pwg=c9c6ca4e4240aef07b502750a5478af638b5aa4588ce4f7b951cfba4f5aa6289
    +test_classification:System
    +name:test_ipp_pwg_envelope_dl_sgray_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_envelope_dl_sgray_16_600dpi
        +guid:c74862e4-c5e2-4eba-9df2-1e7bb0f424a1
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=iso_dl_110x220mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_envelope_dl_sgray_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_dl_110x220mm', default):
        tray.configure_tray(default, 'iso_dl_110x220mm', 'stationery')
        expected_media_size = MediaSize.dlenvelope
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='11000', tempvalue2='ydim', value2='22000')

    printjob.ipp_print(update_dat_file, 'c9c6ca4e4240aef07b502750a5478af638b5aa4588ce4f7b951cfba4f5aa6289')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 10x15cm adobe rgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:10x15cm-adobe-rgb-8-600dpi.pwg=939f7f2f19017561b82ad16b50ffe6d0affae838ebe4468c940875805578435f
    +test_classification:System
    +name:test_ipp_pwg_10x15cm_adobe_rgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_10x15cm_adobe_rgb_8_600dpi
        +guid:07d431bf-7e34-470f-9e52-509d0ead4e6c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=om_small-photo_100x150mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_10x15cm_adobe_rgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('om_small-photo_100x150mm', default):
        tray.configure_tray(default, 'om_small-photo_100x150mm', 'stationery')
        expected_media_size = MediaSize.media100x150
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10000', tempvalue2='ydim', value2='15000')

    printjob.ipp_print(update_dat_file, '939f7f2f19017561b82ad16b50ffe6d0affae838ebe4468c940875805578435f')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C48516849 ipp test for monarch envelope sgray 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Monarch-Envelope-sgray-16-600dpi.pwg=55e4d5330ab9d747b0cc6bd5706162b7ebf624bfb18edf3d5700488cfab0c206
    +test_classification:System
    +name:test_ipp_pwg_monarch_envelope_sgray_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_monarch_envelope_sgray_16_600dpi
        +guid:eaf42561-974c-42bd-8a2c-439271778c7c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_monarch_3.875x7.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_monarch_envelope_sgray_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_size_supported('na_monarch_3.875x7.5in', default):
        tray.configure_tray(default, 'na_monarch_3.875x7.5in', 'stationery')
    elif tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
        expected_media_size = MediaSize.custom
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='9843', tempvalue2='ydim', value2='19050')

    printjob.ipp_print(update_dat_file, '55e4d5330ab9d747b0cc6bd5706162b7ebf624bfb18edf3d5700488cfab0c206')
    tray.reset_trays()

    #verify crc
    outputsaver.save_output()
    current_crc = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(current_crc), "fail on crc mismatch"

    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for pwg executive srgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Executive-srgb-8-300dpi.pwg=758d6e8254fddb2ab31842f10c3a485a0f443d68c2751eb339915ee44fa57656
    +test_classification:System
    +name:test_ipp_pwg_executive_srgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_executive_srgb_8_300dpi
        +guid:2c7915d6-39ed-41ea-be17-8282026410cc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_executive_7.25x10.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_executive_srgb_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_executive_7.25x10.5in', default):
        tray.configure_tray(default, 'na_executive_7.25x10.5in', 'stationery')
        expected_media_size = MediaSize.executive
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='18415', tempvalue2='ydim', value2='26670')

    printjob.ipp_print(update_dat_file, '758d6e8254fddb2ab31842f10c3a485a0f443d68c2751eb339915ee44fa57656')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for jis b5 srgb 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JIS-B5-srgb-8-300dpi.pwg=0999a39b78be5fad0bddfd0c19e2222578277a9b5f651a61234541803526c914
    +test_classification:System
    +name:test_ipp_pwg_jis_b5_srgb_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_jis_b5_srgb_8_300dpi
        +guid:d121eadb-8af7-4bc5-a676-aab673a00fc4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=jis_b5_182x257mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_jis_b5_srgb_8_300dpi(setup_teardown, printjob, outputverifier, tray,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('jis_b5_182x257mm', default):
        tray.configure_tray(default, 'jis_b5_182x257mm', 'stationery')
        expected_media_size = MediaSize.jis_b5
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='18200', tempvalue2='ydim', value2='25700')

    printjob.ipp_print(update_dat_file, '0999a39b78be5fad0bddfd0c19e2222578277a9b5f651a61234541803526c914')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for jis b6 srgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JIS-B6-srgb-8-600dpi.pwg=639071ab50c98a68d3f4a7246b32b2303a2a2c4a33ed2209691a66f362983acc
    +test_classification:System
    +name:test_ipp_pwg_jis_b6_srgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_jis_b6_srgb_8_600dpi
        +guid:c7b580a6-1cff-49ac-b35a-484a99ea9ad0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=jis_b6_128x182mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_jis_b6_srgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('jis_b6_128x182mm', default):
        tray.configure_tray(default, 'jis_b6_128x182mm', 'stationery')
        expected_media_size = MediaSize.jis_b6

    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom

    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='12800', tempvalue2='ydim', value2='18200')

    printjob.ipp_print(update_dat_file, '639071ab50c98a68d3f4a7246b32b2303a2a2c4a33ed2209691a66f362983acc')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177687/C52177689 ipp test for legal srgb 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Legal-srgb-8-600dpi.pwg=9b286327f2b2ae0701433c65d458f02a8900a5960b850212fb9422404d856ad3
    +test_classification:System
    +name:test_ipp_pwg_legal_srgb_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_legal_srgb_8_600dpi
        +guid:26a05c5a-9503-4f99-b6f3-72ce3076e2bb
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_legal_srgb_8_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw, reset_tray):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
        expected_media_size = MediaSize.legal
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='35560')

    printjob.ipp_print(update_dat_file, '9b286327f2b2ae0701433c65d458f02a8900a5960b850212fb9422404d856ad3')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177690 ipp test for letter srgb 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-srgb-16-300dpi.pwg=1d43c24feaf1dcda49c5f63ac9ea9b528cb27038662fcbd9e2d504e295950943
    +test_classification:System
    +name:test_ipp_pwg_letter_srgb_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_letter_srgb_16_300dpi
        +guid:bb608580-47e5-42b3-bdfc-6ac7a5e21b61
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_letter_srgb_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='27940')

    printjob.ipp_print(update_dat_file, '1d43c24feaf1dcda49c5f63ac9ea9b528cb27038662fcbd9e2d504e295950943')
    outputverifier.save_and_parse_output()

    default_source = tray.get_default_source()
    expected_media_size = MediaSize.letter
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(8.5 * job_resolution)
        expected_height = round(11 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for statement srgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Statement-srgb-16-600dpi.pwg=4a51d653da3be82735b227447e32a72d62bf3a2e54233d10d9140395eadf89a8
    +test_classification:System
    +name:test_ipp_pwg_statement_srgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_statement_srgb_16_600dpi
        +guid:12aa9d4f-ad98-4a37-816e-345e3cd75867
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_invoice_5.5x8.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_statement_srgb_16_600dpi(setup_teardown, printjob, outputverifier, tray,outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_invoice_5.5x8.5in', default):
        tray.configure_tray(default, 'na_invoice_5.5x8.5in', 'stationery')
        expected_media_size = MediaSize.statement
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='13970', tempvalue2='ydim', value2='21590')

    printjob.ipp_print(update_dat_file, '4a51d653da3be82735b227447e32a72d62bf3a2e54233d10d9140395eadf89a8')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 3.5x5 adobe rgb 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:3.5x5-adobe-rgb-16-300dpi.pwg=5d11d78769aa692ad577be52ea27f723740451d6a6a0aa05a8f77dfeead1a5a1
    +test_classification:System
    +name:test_ipp_pwg_3_5x5_adobe_rgb_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_3_5x5_adobe_rgb_16_300dpi
        +guid:2bf0c2c4-20a7-4823-bee5-432bcb8880ba
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_3_5x5_adobe_rgb_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    outputsaver.operation_mode('TIFF')
    # 3.5x5 is L
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('om_photo_89x127mm', default):
        tray.configure_tray(default, 'om_photo_89x127mm', 'stationery')
        expected_media_size = MediaSize.photo_l
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='8890', tempvalue2='ydim', value2='12700')

    printjob.ipp_print(update_dat_file, '5d11d78769aa692ad577be52ea27f723740451d6a6a0aa05a8f77dfeead1a5a1', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 3x5 adobe rgb 16 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:3x5-adobe-rgb-16-300dpi.pwg=8975a924501c372df7476f3e6c988021c9cc557508e9a7bd4d0c85fef71fba04
    +test_classification:System
    +name:test_ipp_pwg_3x5_adobe_rgb_16_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_3x5_adobe_rgb_16_300dpi
        +guid:3b7792be-527b-41b8-858a-1386d23c5be0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_3x5_adobe_rgb_16_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_index-3x5_3x5in', default):
        tray.configure_tray(default, 'na_index-3x5_3x5in', 'stationery')
        expected_media_size = MediaSize.photo3x5
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='7620', tempvalue2='ydim', value2='12700')

    printjob.ipp_print(update_dat_file, '8975a924501c372df7476f3e6c988021c9cc557508e9a7bd4d0c85fef71fba04', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 4x6 adobe rgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:4x6-adobe-rgb-16-600dpi.pwg=0741e1385c604d7d94c253dcd8f757d398be37c66b228cbfb7c2085844b6c626
    +test_classification:System
    +name:test_ipp_pwg_4x6_adobe_rgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_4x6_adobe_rgb_16_600dpi
        +guid:b91eb3b2-d373-4d29-9cbd-99f89805e1aa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_4x6_adobe_rgb_16_600dpi(setup_teardown, printjob, outputverifier, outputsaver,tray):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_index-4x6_4x6in', default):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'stationery')
        expected_media_size = MediaSize.photo4x6
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='10160', tempvalue2='ydim', value2='15240')

    printjob.ipp_print(update_dat_file, '0741e1385c604d7d94c253dcd8f757d398be37c66b228cbfb7c2085844b6c626', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputsaver.operation_mode('NONE')
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 5x7 adobe rgb 16 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5x7-adobe-rgb-16-600dpi.pwg=1668068dd13c382c8cf7704cd5843fd7e91328bc6d5802a91fe2ee3fb6d88139
    +test_classification:System
    +name:test_ipp_pwg_5x7_adobe_rgb_16_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_5x7_adobe_rgb_16_600dpi
        +guid:d7a63664-af45-430c-8773-b60663b1a4e0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_5x7_adobe_rgb_16_600dpi(setup_teardown, printjob, outputverifier, tray, outputsaver):
    logging.info("For failed print job, no PDL_PAGE_CRC in PrintIntentPage file. No need to check CRC for this case.")
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_5x7_5x7in', default):
        tray.configure_tray(default, 'na_5x7_5x7in', 'stationery')
        expected_media_size = MediaSize.photo5x7
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='12700', tempvalue2='ydim', value2='17780')

    printjob.ipp_print(update_dat_file, '1668068dd13c382c8cf7704cd5843fd7e91328bc6d5802a91fe2ee3fb6d88139', 'FAILED')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 5x8 sgray 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5x8-sgray-8-300dpi.pwg=99e799a4eed7fbf41a6030b2412e205296f87e652aa7f71e956c2677ec362ed3
    +test_classification:System
    +name:test_ipp_pwg_5x8_sgray_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_5x8_sgray_8_300dpi
        +guid:4ed6e5c6-ae5c-4d2c-98ea-714b9eba7c98
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_index-5x8_5x8in

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_5x8_sgray_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_index-5x8_5x8in', default):
        tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')
        expected_media_size = MediaSize.photo5x8
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='12700', tempvalue2='ydim', value2='20320')

    printjob.ipp_print(update_dat_file, '99e799a4eed7fbf41a6030b2412e205296f87e652aa7f71e956c2677ec362ed3')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 8.5x13 sgray 8 300dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8.5x13-sgray-8-300dpi.pwg=555f98c44ad09a8d73c7300ed1ded58aae7c90634a4dfbc2118cb3b599309e9c
    +test_classification:System
    +name:test_ipp_pwg_8_5x13_sgray_8_300dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_8_5x13_sgray_8_300dpi
        +guid:928d3ade-ca5e-4a29-bbe3-48b89786c8bf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_foolscap_8.5x13in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_8_5x13_sgray_8_300dpi(setup_teardown, printjob, outputverifier, tray, outputsaver, udw):
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_foolscap_8.5x13in', default):
        tray.configure_tray(default, 'na_foolscap_8.5x13in', 'stationery')
        expected_media_size = MediaSize.foolscap
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='33020')

    printjob.ipp_print(update_dat_file, '555f98c44ad09a8d73c7300ed1ded58aae7c90634a4dfbc2118cb3b599309e9c')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for 8x10 sgray 8 600dpi
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8x10-sgray-8-600dpi.pwg=629cdd366593cad13183c03ed1cbfb2d5b919f36b647eafbe251fc69dddbe6d6
    +test_classification:System
    +name:test_ipp_pwg_8x10_sgray_8_600dpi
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_8x10_sgray_8_600dpi
        +guid:00bddff9-d1d4-4e71-883a-b41eb6454333
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_govt-letter_8x10in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_8x10_sgray_8_600dpi(setup_teardown, printjob, outputverifier, tray):
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_govt-letter_8x10in', default):
        tray.configure_tray(default, 'na_govt-letter_8x10in', 'stationery')
        expected_media_size = MediaSize.govt_letter
    elif tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='20320', tempvalue2='ydim', value2='25400')

    printjob.ipp_print(update_dat_file, '629cdd366593cad13183c03ed1cbfb2d5b919f36b647eafbe251fc69dddbe6d6')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for print a4 600dpi sgray 8
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4-sgray-8-600dpi.pwg=b50d39b6eb0261d533b8881bcaa48d243d8353ec827178f8792bb100bb7daf38
    +test_classification:System
    +name:test_ipp_pwg_print_a4_600dpi_sgray_8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_print_a4_600dpi_sgray_8
        +guid:8b410fb1-2b3f-4cd2-a899-a97d912817cc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_print_a4_600dpi_sgray_8(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
        expected_media_size = MediaSize.a4
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21000', tempvalue2='ydim', value2='29700')

    printjob.ipp_print(update_dat_file, 'b50d39b6eb0261d533b8881bcaa48d243d8353ec827178f8792bb100bb7daf38')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for print legal 600dpi srgb 8
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Legal-srgb-8-600dpi.pwg=9b286327f2b2ae0701433c65d458f02a8900a5960b850212fb9422404d856ad3
    +test_classification:System
    +name:test_ipp_pwg_print_legal_600dpi_srgb_8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_print_legal_600dpi_srgb_8
        +guid:ee513086-3f12-4128-8081-19ebb5af4f3e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP & MediaSizeSupported=na_legal_8.5x14in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_print_legal_600dpi_srgb_8(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
        expected_media_size = MediaSize.legal
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='35560')

    printjob.ipp_print(update_dat_file, '9b286327f2b2ae0701433c65d458f02a8900a5960b850212fb9422404d856ad3')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:ipp test for print letter 300dpi srgb 16
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-srgb-16-300dpi.pwg=1d43c24feaf1dcda49c5f63ac9ea9b528cb27038662fcbd9e2d504e295950943
    +test_classification:System
    +name:test_ipp_pwg_print_letter_300dpi_srgb_16
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pwg_print_letter_300dpi_srgb_16
        +guid:b6d37074-15e2-4b42-8247-1f17e0a5bb95
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster & PrintProtocols=IPP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pwg_print_letter_300dpi_srgb_16(setup_teardown, printjob, outputverifier, tray, outputsaver, cdm):
    outputsaver.operation_mode('TIFF')

    update_dat_file = printjob.copy_file_to_output_folder(PRINT_MEDIA_SIZE_TEST_FILE_PATH)
    update_ipp_datfile(update_dat_file, tempvalue1='xdim', value1='21590', tempvalue2='ydim', value2='27940')

    printjob.ipp_print(update_dat_file, '1d43c24feaf1dcda49c5f63ac9ea9b528cb27038662fcbd9e2d504e295950943')
    outputverifier.save_and_parse_output()

    default_source = tray.get_default_source()
    expected_media_size = MediaSize.letter
    if default_source in tray.rolls:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        #verify letter dimensions
        expected_width = round(8.5 * job_resolution)
        expected_height = round(11 * job_resolution)

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputsaver.operation_mode('NONE')

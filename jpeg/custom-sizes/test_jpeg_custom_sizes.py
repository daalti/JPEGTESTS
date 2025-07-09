from dunetuf.print.output.intents import Intents, MediaSize
import logging
from dunetuf.print.print_common_types import MediaInputIds,  MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using CS(300X200)-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CS300X200-150-L.jpg=98b2abe4245f479ed174d858e18953abd74f50c131b1accb82141c9c190657c0
    +test_classification:System
    +name:test_jpeg_custom_size_300x200_150_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_300x200_150_landscape
        +guid:b24d9120-5f08-4cec-ba9f-0b68957c7b2a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_300x200_150_landscape(setup_teardown, printjob, outputverifier,outputsaver,udw,tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('98b2abe4245f479ed174d858e18953abd74f50c131b1accb82141c9c190657c0')

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using CS(300X200)-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CS300X200-231-L.jpg=cda4d59f5ef4aa6c7b7a1ab26a50ce25e3dede1ab33db39c8ea1dfe9cd81a4b1
    +test_classification:System
    +name:test_jpeg_custom_size_300x200_231_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_300x200_231_landscape
        +guid:c5ca2c3a-2f94-4bf0-89d7-4dd9a069fe09
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_300x200_231_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')


    printjob.print_verify('cda4d59f5ef4aa6c7b7a1ab26a50ce25e3dede1ab33db39c8ea1dfe9cd81a4b1')

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.outputsaver.operation_mode('NONE')
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using CS(300X200)-300-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CS300X200-300-L.jpg=e764a78f35cd170ec6be58b5b3b528d0beb822e7165d79f0bef48ddb8be4f50b
    +test_classification:System
    +name:test_jpeg_custom_size_300x200_300_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_300x200_300_landscape
        +guid:b25a0cff-42ff-462b-a307-05ca889ae7ea
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_300x200_300_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.custom

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
        expected_media_size = MediaSize.custom
    else:
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom

    printjob.print_verify('e764a78f35cd170ec6be58b5b3b528d0beb822e7165d79f0bef48ddb8be4f50b')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using CS(300X200)-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:CS300X200-600-L.jpg=da2f863844d9803c20e43af79113f5dc247548f79daccc3f8c34be97374d4f6f
    +test_classification:System
    +name:test_jpeg_custom_size_300x200_600_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_300x200_600_landscape
        +guid:0931fdbd-3524-4fad-9402-845dfc902a3c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_300x200_600_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.custom

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
        expected_media_size = MediaSize.custom
    else:
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom

    printjob.print_verify('da2f863844d9803c20e43af79113f5dc247548f79daccc3f8c34be97374d4f6f')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using cs(200X300)-600-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cs200X300-600-P.jpg=8e3bb43894bdac34f661ab3b93d9494468671f0677715dc315108c3873f54658
    +test_classification:System
    +name:test_jpeg_custom_size_200X300_600_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_200X300_600_portrait
        +guid:5cd23bcc-489a-44a4-8ef3-b1cef9a55060
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_200X300_600_portrait(setup_teardown, printjob, outputverifier, tray, print_emulation, configuration):
    outputverifier.outputsaver.operation_mode('TIFF')
    expected_media_size = MediaSize.custom
    default = tray.get_default_source()
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('anycustom', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
            print_emulation.tray.close(tray1)
    else:
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
            expected_media_size = MediaSize.custom
        else:
            tray.configure_tray(default, 'custom', 'stationery')
            expected_media_size = MediaSize.custom

    printjob.print_verify('8e3bb43894bdac34f661ab3b93d9494468671f0677715dc315108c3873f54658')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using cs(200X300)-150-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cs200X300-150-P.jpg=d5c61c429865ee5df8b12690ad9e017b724e8aad1d2d562a5daafac7f5b14c5e
    +test_classification:System
    +name:test_jpeg_custom_size_200x300_150_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_200x300_150_portrait
        +guid:675f7e65-c619-4e49-8dbc-75ce5d564b36
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_200x300_150_portrait(setup_teardown, printjob, outputverifier, udw, outputsaver, tray,print_emulation,configuration):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('anycustom', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
            print_emulation.tray.close(tray1)
    else:
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('d5c61c429865ee5df8b12690ad9e017b724e8aad1d2d562a5daafac7f5b14c5e')
    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using cs(200X300)-231-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cs200X300-231-P.jpg=fdddf6538a2e6bb0830aa6b022da3f7c3f50d00bbb0ee82d9b3417f76307e519
    +test_classification:System
    +name:test_jpeg_custom_size_200x300_231_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_200x300_231_portrait
        +guid:f0af8603-bfb5-4249-805c-ee0b21501bae
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_200x300_231_portrait(setup_teardown, printjob, print_emulation,configuration, outputverifier, udw, outputsaver, tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        tray1 = MediaInputIds.Tray1.name
        if tray.is_size_supported('anycustom', 'tray-1'):
            print_emulation.tray.open(tray1)
            print_emulation.tray.load(tray1, "Custom", MediaType.Plain.name)
            print_emulation.tray.close(tray1)
    else:
        if tray.is_size_supported('anycustom', default):
            tray.configure_tray(default, 'anycustom', 'stationery')
        else:
            tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('fdddf6538a2e6bb0830aa6b022da3f7c3f50d00bbb0ee82d9b3417f76307e519')

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using cs(200X300)-300-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:cs200X300-300-P.jpg=c27a6a5933434299e7cb8ec2804bbf807c4f7adcbbdaa5bc39e7a91bc5082ac2
    +test_classification:System
    +name:test_jpeg_custom_size_200x300_300_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_custom_size_200x300_300_portrait
        +guid:70fd3473-c0ea-46df-85b6-b6c36b7814bc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_custom_size_200x300_300_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.custom

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
        expected_media_size = MediaSize.custom
    else:
        tray.configure_tray(default, 'custom', 'stationery')
        expected_media_size = MediaSize.custom

    printjob.print_verify('c27a6a5933434299e7cb8ec2804bbf807c4f7adcbbdaa5bc39e7a91bc5082ac2')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')

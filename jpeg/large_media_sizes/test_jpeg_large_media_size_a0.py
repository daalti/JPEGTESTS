from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source

A0_WIDTH_IN_INCH = 841000 / 25400.0
A0_HEIGHT_IN_INCH = 1189000 / 25400.0
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A0-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:800
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-150-L.jpg=513d5fdcf318c017102091023daee87d2fa69ace1bfbb8b62aec8f81cd0ddcca
    +test_classification:System
    +name:test_jpeg_large_media_size_a0_150_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a0_150_landscape
        +guid:ffa5ffb7-42eb-40c1-a6db-e627de1ece9a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a0_150_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    printjob.print_verify('513d5fdcf318c017102091023daee87d2fa69ace1bfbb8b62aec8f81cd0ddcca',timeout=720)
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A0-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-231-L.jpg=83c9b8a78e0aa5ee8c3dffa99eb67744678c9d1a53048675bb2ce2493e3e4b14
    +test_classification:System
    +name:test_jpeg_large_media_size_a0_231_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a0_231_landscape
        +guid:094f8e20-083e-4384-a887-b5157e295a5c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a0_231_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    printjob.print_verify('83c9b8a78e0aa5ee8c3dffa99eb67744678c9d1a53048675bb2ce2493e3e4b14')
    tray.reset_trays()
    outputverifier.save_and_parse_output()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A0-300-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-300-L.jpg=2d582a10f32bfcbdb87a7a8fbc8b97c28712c7f125b2e91b146340426f90237d
    +test_classification:System
    +name:test_jpeg_large_media_size_a0_300_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a0_300_landscape
        +guid:e37e9c1d-bc16-4077-8b61-40a2e5bf2a0a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a0_300_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    printjob.print_verify('2d582a10f32bfcbdb87a7a8fbc8b97c28712c7f125b2e91b146340426f90237d')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A0-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-600-L.jpg=7cb450b01b282a6ce2117eb3357f9c72335996e96639de9ccf8ad60ae80ddd29
    +test_classification:System
    +name:test_jpeg_large_media_size_a0_600_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a0_600_landscape
        +guid:f147b35a-52dd-4aca-a242-209779fa2d77
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a0_600_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    printjob.print_verify('7cb450b01b282a6ce2117eb3357f9c72335996e96639de9ccf8ad60ae80ddd29', timeout=300)
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A0-72-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A0-72-L.jpg=9b43011721bb31f222ba23e8830d8e3487b12bfd342fd52813f06ef3c35d03fd
    +test_classification:System
    +name:test_jpeg_large_media_size_a0_72_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a0_72_landscape
        +guid:de08b9ba-d724-4168-aefc-57453157c1a8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a0_72_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    
    expected_media_size = MediaSize.letter
    printjob.print_verify('9b43011721bb31f222ba23e8830d8e3487b12bfd342fd52813f06ef3c35d03fd')
    outputverifier.save_and_parse_output()

    # expecting large media sizes to be printed on rolls
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        # verify A0 dimensions. Landscape width too large, so image will be rotated
        expected_width = round(A0_WIDTH_IN_INCH * job_resolution)
        expected_height = round(A0_HEIGHT_IN_INCH * job_resolution)
        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)

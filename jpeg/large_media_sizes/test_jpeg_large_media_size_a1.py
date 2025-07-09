from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source

A1_WIDTH_IN_INCH = 594000 / 25400
A1_HEIGHT_IN_INCH = 841000 / 25400
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-150-L.jpg=6b9fb0bfbd3dac81fc5f48347ddd337f30a1ad03e2af9bb541ec251142ca024d
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_150_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_150_landscape
        +guid:53a03f39-21b0-4f83-b2ac-c08227bd4f94
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_150_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('6b9fb0bfbd3dac81fc5f48347ddd337f30a1ad03e2af9bb541ec251142ca024d')
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.letter
    #expecting large media sizes to be printed on rolls
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
    
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)

    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-231-L.jpg=0268b87aa87b04ac03087e8c414f083298dc60ffc655882839b25e98702fe906
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_231_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_231_landscape
        +guid:9f359f71-f54b-471a-8696-fea0410591b2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_231_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('0268b87aa87b04ac03087e8c414f083298dc60ffc655882839b25e98702fe906')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-600-L.jpg=c4ec10f90c24466ce65a838d090a7297d47b83cc1b287b22a7ba468392983ce2
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_600_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_600_landscape
        +guid:1188a0d3-b5d2-41c5-be66-e919badae431
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_600_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('c4ec10f90c24466ce65a838d090a7297d47b83cc1b287b22a7ba468392983ce2')
    tray.reset_trays()
    
    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-150-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-150-P.jpg=4fa0a710aa32e40d244748ff4ffd60c3d1d440d31003ad5c898c0c93f1aab914
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_150_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_150_portrait
        +guid:8d806d35-cc13-49c0-94df-bfaa95e57e46
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_150_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('4fa0a710aa32e40d244748ff4ffd60c3d1d440d31003ad5c898c0c93f1aab914')
    outputverifier.save_and_parse_output()
    expected_media_size = MediaSize.letter
    # expecting large media sizes to be printed on rolls
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        autorotate_enabled = outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
        # verify A1 dimensions
        expected_width = round(A1_WIDTH_IN_INCH * job_resolution)
        expected_height = round(A1_HEIGHT_IN_INCH * job_resolution)

        if autorotate_enabled:
            expected_height, expected_width = expected_width, expected_height

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-231-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-231-P.jpg=9c3125a439ca88db6e0df33be1cbb786ad07e320e6c1a3a02876f614baf1a89c
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_231_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_231_portrait
        +guid:605ce56a-8a8c-417a-bd2d-e7529b8e45c9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_231_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('9c3125a439ca88db6e0df33be1cbb786ad07e320e6c1a3a02876f614baf1a89c')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-300-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-300-P.jpg=c00d2dfa17efe5d98c11979cdbc18b514f04d4462cd3fe79eeecfcb107d94e22
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_300_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_300_portrait
        +guid:39db709f-5f5f-4680-aecc-46897f70fb72
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_300_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('c00d2dfa17efe5d98c11979cdbc18b514f04d4462cd3fe79eeecfcb107d94e22')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-600-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-600-P.jpg=194d330ac173675bf2b0e445cc1a42971bc90cf67fb7503d0d860938680dc75f
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_600_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_600_portrait
        +guid:2761d861-eefc-4d20-aad6-5b78fbff003c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_600_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('194d330ac173675bf2b0e445cc1a42971bc90cf67fb7503d0d860938680dc75f')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A1-72-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A1-72-P.jpg=546bd634cfc1d42f3a3f2cb2067061599d02f89fc07e0f8e9b9f98eba977c760
    +test_classification:System
    +name:test_jpeg_large_media_size_a1_72_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a1_72_portrait
        +guid:5e95567d-3240-4e37-a605-7b0e5abebdf8
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a1_72_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('546bd634cfc1d42f3a3f2cb2067061599d02f89fc07e0f8e9b9f98eba977c760')
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.letter
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        autorotate_enabled = outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
        # verify A1 dimensions
        expected_width = round(A1_WIDTH_IN_INCH * job_resolution)
        expected_height = round(A1_HEIGHT_IN_INCH * job_resolution)

        if autorotate_enabled:
            expected_height, expected_width = expected_width, expected_height

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)
         

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')

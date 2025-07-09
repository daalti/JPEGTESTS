from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, MediaSizeID, get_media_source

A2_WIDTH_IN_INCH = 420000 / 25400
A2_HEIGHT_IN_INCH = 594000 / 25400

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-150-L.jpg=0c0c9cb7efafcd92862dc8f5bc3f4162b22c5fd073474314e61a186ac57213b0
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_150_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_150_landscape
        +guid:ddaf1d53-caa2-4fbe-abb5-44a4707b15b5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a1_594x841mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_150_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('0c0c9cb7efafcd92862dc8f5bc3f4162b22c5fd073474314e61a186ac57213b0')
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.letter
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        expected_width = round(A2_HEIGHT_IN_INCH * job_resolution)
        expected_height = round(A2_WIDTH_IN_INCH * job_resolution)
        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-231-L.jpg=d3aa431d8e5e8642c464c5847a85870e24a18548a48434a17d18bfbee779beef
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_231_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_231_landscape
        +guid:4f9432fb-cbcf-4ca3-9d2a-5bb7e82f3f11
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_231_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('d3aa431d8e5e8642c464c5847a85870e24a18548a48434a17d18bfbee779beef')
    tray.reset_trays()
    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-300-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-300-L.jpg=5d3834edeb0fe10dc8a3f6efe0f775f1ca834efbaa6c1e774bb9b7f69534c1df
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_300_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_300_landscape
        +guid:4c29da12-2246-4ec9-9181-723c0488756e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_300_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('5d3834edeb0fe10dc8a3f6efe0f775f1ca834efbaa6c1e774bb9b7f69534c1df')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-600-L.jpg=0c3df6b2d0193e7a5513153c1c9c4302d17b07e27954d905e5e7e158e7a2b387
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_600_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_600_landscape
        +guid:73e11e1b-bc84-4ea9-9d28-a75ffc3daaa2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_600_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('0c3df6b2d0193e7a5513153c1c9c4302d17b07e27954d905e5e7e158e7a2b387')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-150-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-150-P.jpg=dd8e1d2006c6aa7b9fb430afe9c86f8b613b7b668e44bf78b1639a94a1d747a9
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_150_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_150_portrait
        +guid:ff57918c-671d-464b-86e0-4bd11da169fa
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_150_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('dd8e1d2006c6aa7b9fb430afe9c86f8b613b7b668e44bf78b1639a94a1d747a9')
    outputverifier.save_and_parse_output()

    expected_media_size = MediaSize.letter
    # expecting large media sizes to be printed on rolls
    if tray.rolls is not None:
        expected_media_size = MediaSize.custom
        job_resolution = outputverifier.get_intent(Intents.printintent)[0].resolution
        autorotate_enabled = outputverifier.get_intent(Intents.printintent)[0].autorotate_enable
        #verify a2 dimensions
        expected_width = round(A2_WIDTH_IN_INCH * job_resolution)
        expected_height = round(A2_HEIGHT_IN_INCH * job_resolution)
        if autorotate_enabled:
            expected_height, expected_width = expected_width, expected_height

        outputverifier.verify_page_width(Intents.printintent, expected_width, redundance_accepted=1)
        outputverifier.verify_page_height(Intents.printintent, expected_height, redundance_accepted=1)

    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-231-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-231-P.jpg=2434111e88da7bf86923ededbe8bab58f445c57573a70d149f51e8c4b84b5d55
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_231_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_231_portrait
        +guid:0a877953-e6f1-418e-b23f-fc641ce93c58
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_231_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('2434111e88da7bf86923ededbe8bab58f445c57573a70d149f51e8c4b84b5d55')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-300-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-300-P.jpg=4586844286746a4283fb829956e33d39452f64c977f7516614818926cc42bf07
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_300_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_300_portrait
        +guid:94ef2b78-4bc1-496f-8a93-de39eca1cff6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_300_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('4586844286746a4283fb829956e33d39452f64c977f7516614818926cc42bf07')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A2-600-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A2-600-P.jpg=2f75e1aa07692c43d6e4de5a0fab8bab6e85bac95689caa2a42143c4292656f7
    +test_classification:System
    +name:test_jpeg_large_media_size_a2_600_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a2_600_portrait
        +guid:87b3596d-aaae-40dd-8813-93f9d7ef3091
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a2_420x594mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a2_600_portrait(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('2f75e1aa07692c43d6e4de5a0fab8bab6e85bac95689caa2a42143c4292656f7')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')

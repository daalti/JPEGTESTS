from dunetuf.print.output.intents import Intents, MediaSize, MediaSource, get_media_source


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-150-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-150-L.jpg=44f6cf3630ed32881134bea9153428d57c69fde0efbe38da68a24e95ff2c68dc
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_150_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_150_landscape
        +guid:701430b5-634c-4cbb-9498-bbebbf8c489a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & MediaInputInstalled = Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_150_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('44f6cf3630ed32881134bea9153428d57c69fde0efbe38da68a24e95ff2c68dc')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-231-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-231-L.jpg=98a7b77efdee8efca9bc37d2f93b6b081e78d7aa3d13ccea2260e25ef1eee317
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_231_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_231_landscape
        +guid:e656cdcf-2472-4160-8391-bbf6b6502ddc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & MediaInputInstalled = Tray1

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_231_landscape(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('98a7b77efdee8efca9bc37d2f93b6b081e78d7aa3d13ccea2260e25ef1eee317')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-300-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-300-L.jpg=d7d4d21b5d1b3269b57c3208c0e3272b162c439b1a9a40dd01981358dcd2eb62
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_300_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_300_landscape
        +guid:ca7a2d47-43d8-4f3e-8027-d08d7e8ff64a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm & EngineFirmwareFamily=Maia

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_300_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('d7d4d21b5d1b3269b57c3208c0e3272b162c439b1a9a40dd01981358dcd2eb62')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-600-L.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files: A3-600-L.jpg=5ecd428b320c23d6f899cb26277f73ffbfdee376ad8625d1189ca6eff6140013
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_600_landscape
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_600_landscape
        +guid:d10ceb63-91a3-4a6b-8f98-485d0e0f31e3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a0_841x1189mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_600_landscape(setup_teardown, printjob, outputverifier, tray, cdm):
    outputverifier.outputsaver.operation_mode('TIFF')

    printjob.print_verify('5ecd428b320c23d6f899cb26277f73ffbfdee376ad8625d1189ca6eff6140013')
    tray.reset_trays()

    media_source = get_media_source(tray.rolls[0])

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
    outputverifier.verify_media_source(Intents.printintent, media_source)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-150-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-150-P.jpg=52e22db4d0237e6cf053a243d10b49e773ca4a0e5dbc5ebae3f48c8e87cefeba
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_150_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_150_portrait
        +guid:7a89cef3-bc55-441d-9ec6-3c25f9780b35
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_150_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('52e22db4d0237e6cf053a243d10b49e773ca4a0e5dbc5ebae3f48c8e87cefeba')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-231-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-231-P.jpg=8b9f79cd74a56bb19019053cd9500429069e2afa20932b0aad2acbb11c49a30e
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_231_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_231_portrait
        +guid:2c5c7d56-7471-41d3-a580-dbe5959306ae
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_231_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('8b9f79cd74a56bb19019053cd9500429069e2afa20932b0aad2acbb11c49a30e')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-300-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-300-P.jpg=93caf9440369f33424aaeebe4c1238e86c29625d08e1cef696d837aad108bbc7
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_300_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_300_portrait
        +guid:c897c3b0-26be-45af-8ae7-ee50a933687d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_300_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('93caf9440369f33424aaeebe4c1238e86c29625d08e1cef696d837aad108bbc7')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using A3-600-P.jpg
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3-600-P.jpg=d93ee93e25e90f605960ba6df9fd3ea2e0b0b733c5bfabebfa8a202b4fa771d2
    +test_classification:System
    +name:test_jpeg_large_media_size_a3_600_portrait
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_large_media_size_a3_600_portrait
        +guid:baaf184e-8512-44ad-af6d-6a4a0bad0351
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & MediaSizeSupported=iso_a3_297x420mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_large_media_size_a3_600_portrait(setup_teardown, printjob, outputverifier, tray):
    outputverifier.outputsaver.operation_mode('TIFF')

    expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')
        expected_media_size = MediaSize.a3

    printjob.print_verify('d93ee93e25e90f605960ba6df9fd3ea2e0b0b733c5bfabebfa8a202b4fa771d2')
    tray.reset_trays()

    outputverifier.save_and_parse_output()
    outputverifier.verify_media_size(Intents.printintent, expected_media_size)
    outputverifier.outputsaver.operation_mode('NONE')

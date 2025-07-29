import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a basic job without white
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114994
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:color_basic_CMYKLites.rs=8bc2bb983f2403da91bf59239bffd046943b06b7f872353d9d0a8b416bb95c87
    +test_classification:System
    +name:test_rs_color_basic_cmyklites_job_print
    +test:
        +title:test_rs_color_basic_cmyklites_job_print
        +guid:94cfe163-5436-4d26-8505-522763e9b721
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_color_basic_cmyklites_job_print(setup_teardown, printjob, outputsaver, tcl):

    # Avoid the error from the supplies handling component for print a job color with white ph
    print(tcl.execute("SuppliesHandlingManagerUw setByPassMode"))

    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    printjob.print_verify("8bc2bb983f2403da91bf59239bffd046943b06b7f872353d9d0a8b416bb95c87", timeout=120)
    logging.info("color_basic_CMYKLites.rs - Print job completed successfully")

    expected_crc = ["0x59414912"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("color_basic_CMYKLites.rs - Checksum(s) verified successfully")

    # Enable checks at supplies handling component
    print(tcl.execute("SuppliesHandlingManagerUw setCheckMode"))



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode spot
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114994
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:white_basic_SPOT_v2_OK.rs=aa50b55926fe642d96ca80041ef124d320c8ce9ff0797b24fcae828fe43e20a4
    +test_classification:System
    +name:test_rs_white_basic_spot_job_print
    +test:
        +title:test_rs_white_basic_spot_job_print
        +guid:80a84e5f-5571-44d3-9edd-2b0fad4b38c0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_white_basic_spot_job_print(setup_teardown, printjob, outputsaver, tcl, tray):

    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    # Configure the simulator with adhesive transparent media
    tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")

    printjob.print_verify("aa50b55926fe642d96ca80041ef124d320c8ce9ff0797b24fcae828fe43e20a4", timeout=120)
    logging.info("white_basic_SPOT_v2_OK.rs - Print job completed successfully")

    expected_crc = ["0x2a648a1f"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("white_basic_SPOT_v2_OK.rs - Checksum(s) verified successfully")



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode underflood and whiteshrink disabled
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114994
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:white_basic_no_spot_UF_wshrink_disabled.rs=b901b7b736492ff53ee3a4269e836d89df4e22d8cd07c9b14ecde87c3a8a3094
    +test_classification:System
    +name:test_rs_white_basic_underflood_disabled_whiteshrink_job_print
    +test:
        +title:test_rs_white_basic_underflood_disabled_whiteshrink_job_print
        +guid:440dc73f-47f0-49cd-ac80-082ed6135302
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_white_basic_underflood_disabled_whiteshrink_job_print(setup_teardown, printjob, outputsaver, tcl, tray):

    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    # Configure the simulator with adhesive transparent media
    tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")

    printjob.print_verify("b901b7b736492ff53ee3a4269e836d89df4e22d8cd07c9b14ecde87c3a8a3094", timeout=120)
    logging.info("white_basic_no_spot_UF_wshrink_disabled.rs - Print job completed successfully")

    expected_crc = ["0x2a648a1f"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("white_basic_no_spot_UF_wshrink_disabled.rs - Checksum(s) verified successfully")



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode underflood and whiteshrink enabled
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114994
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:white_basic_no_spot_UF_wshrink_enabled.rs=f49dc7a6b330c9f10a2ae964c35c80c8a80e6b7860917954593eb854d52d2b45
    +test_classification:System
    +name:test_rs_white_basic_underflood_enabled_whiteshrink_job_print
    +test:
        +title:test_rs_white_basic_underflood_enabled_whiteshrink_job_print
        +guid:fbe4c7c6-3a43-457e-bb58-bebe47bf5052
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_white_basic_underflood_enabled_whiteshrink_job_print(setup_teardown, printjob, outputsaver, tcl):

    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    printjob.print_verify("f49dc7a6b330c9f10a2ae964c35c80c8a80e6b7860917954593eb854d52d2b45", timeout=120)
    logging.info("white_basic_no_spot_UF_wshrink_enabled.rs - Print job completed successfully")

    expected_crc = ["0xe54c6249"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("white_basic_no_spot_UF_wshrink_enabled.rs - Checksum(s) verified successfully")



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the Sunspot RasterStreamPlanarICF PDL by printing a white job in mode sandwich
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-114994
    +timeout:120
    +asset:LFP
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:white_japan_SANDWICH_sw3l.rs=65728c71f41a75e5184681ebf962957baaef56d4fb5c5126639654cc136d09a4
    +test_classification:System
    +name:test_rs_white_sandwich_sw3l_job_print
    +test:
        +title:test_rs_white_sandwich_sw3l_job_print
        +guid:ee8992a9-5c91-486d-835f-ddd2882b1b28
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_white_sandwich_sw3l_job_print(setup_teardown, printjob, outputsaver, tcl, tray):

    # CRC will be calculated using the payload of the RasterData
    outputsaver.operation_mode('CRC')

    # Configure the simulator with adhesive transparent media
    tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
    
    printjob.print_verify("65728c71f41a75e5184681ebf962957baaef56d4fb5c5126639654cc136d09a4", timeout=120)
    logging.info("white_japan_SANDWICH_sw3l.rs - Print job completed successfully")

    expected_crc = ["0x32c51ce0"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("white_japan_SANDWICH_sw3l.rs - Checksum(s) verified successfully")
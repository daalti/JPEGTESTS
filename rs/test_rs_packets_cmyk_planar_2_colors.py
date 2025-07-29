import pytest
import logging
import time

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_rs_packets_cmyk_planar_2_colors
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-3969
    +timeout:180
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +test_classification:System
    +name:test_rs_packets_cmyk_planar_2_colors
    +test:
        +title:test_rs_packets_cmyk_planar_2_colors
        +guid:7f977362-8e29-11eb-ac51-c309509e37be
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=MaiaLatex & DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_packets_cmyk_planar_2_colors(setup_teardown, printjob, outputsaver):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8', timeout=300)
    logging.info("packets_cmyk_planar_2_colors.rs - Print job completed successfully")

    expected_crc = ["0xa32323da"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("packets_cmyk_planar_2_colors.rs - Checksum(s) verified successfully")


@pytest.fixture(autouse=True)
def setup_teardown_print_accelerator(tclMaia, tcl):
    """Setup/teardown fixture for test_rs_packets_cmyk_planar_2_colors"""
    logging.info('-- SETUP test_rs_packets_cmyk_planar_2_colors --')

    # Avoid the error from the supplies handling component for print a job color with white ph
    tcl.execute("SuppliesHandlingManagerUw setByPassMode")

    try:
        # Set standard MarMenor
        tclMaia.execute("set previousMM [InstantiationService getStringConstant ServicingScript CONFIGURATION_FILE]")

        # Disable servicing by configuring the default MarMenor with an empty one
        tclMaia.execute("InstantiationService setStringConstant ServicingScript CONFIGURATION_FILE TESTING/MarMenor_Empty.xml")
        tclMaia.execute("ServicingEngine reloadModule")

        # Disable heater
        tclMaia.execute("MediaHeaterManager enableHeater 0")

    except ConnectionRefusedError:
        logging.info('Test running on QEMU, these commands are not supported (Setup does not apply)') 

    # Run the test with custom servicing and heater disabled
    yield

    logging.info('-- TEARDOWN test_rs_packets_cmyk_planar_2_colors --')

    try:
        # Reload the standard MarMenor
        tclMaia.execute("InstantiationService setStringConstant ServicingScript CONFIGURATION_FILE $previousMM")
        tclMaia.execute("ServicingEngine reloadModule")

        # Enable heater
        tclMaia.execute("MediaHeaterManager enableHeater 1")

    except ConnectionRefusedError:
        logging.info('Test running on QEMU, these commands are not supported (Teardown does not apply)') 
    
    # Enable checks at supplies handling component
    tcl.execute("SuppliesHandlingManagerUw setCheckMode")
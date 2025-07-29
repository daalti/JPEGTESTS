import pytest, logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Print job file Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-4072
    +timeout:800
    +asset:PDL_Print
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst=fda544f509127aed115c2f9291f057e16b793b52c79a43d9352fa94079f9f6c9
    +test_classification:system
    +name:test_rs_cannabi_gold_checksum
    +test:
        +title:test_rs_cannabi_gold_checksum
        +guid:33da9390-c2c8-11eb-9197-5b4a27e3061c
        +dut:
            +type:Simulator, Emulator
            +configuration:PrintEngineType=MaiaLatex & DocumentFormat=RasterStreamPlanarICF
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_cannabi_gold_checksum(setup_teardown, printjob, outputsaver, tcl):

    # Avoid the error from the supplies handling component when printing a color job with white ph
    print(tcl.execute("SuppliesHandlingManagerUw setByPassMode"))

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('fda544f509127aed115c2f9291f057e16b793b52c79a43d9352fa94079f9f6c9', timeout=700)
    logging.info("rs Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst - Print job completed successfully")

    expected_crc = ["0xb193b7ed"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("rs Cannabi_Gold_Sticker_SMALL_MOSAICO.tif--8p_6c_36ng.rst - Checksum(s) verified successfully")
   
    # Enable checks at supplies handling component
    print(tcl.execute("SuppliesHandlingManagerUw setCheckMode"))
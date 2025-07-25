import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file bolly.wood_fastOFF_150_18x25 and check CRC
    +test_tier:1
    +is_manual:False
    +reqid:LFPSWQAA-5786
    +timeout:350
    +asset:LFP
    +test_framework:TUF
    +delivery_team:LFP 
    +feature_team:ProductQA
    +external_files:bolly.wood_fastOFF_150_18x25.hpgl2=26a6e9e184d4857fb9a798d433c5c246c452337ab40accd9d864fdd512b0f3d5
    +test_classification:System
    +name:test_hpgl2_print_and_check_CRC
    +test:
        +title:test_hpgl2_print_and_check_CRC
        +guid:abeb1716-5981-4486-89ed-f530aa2405b3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_hpgl2_print_and_check_CRC(setup_teardown, printjob, outputsaver):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('26a6e9e184d4857fb9a798d433c5c246c452337ab40accd9d864fdd512b0f3d5', 'SUCCESS', 300, 1)
    logging.info("HPGL2 bolly.wood_fastOFF_150_18x25.hpgl2 - Print job completed successfully")

    if outputsaver.configuration.productname == "jupiter":
        crc_expected = ["0xa499de78"]
    elif outputsaver.configuration.productname.startswith("flare") or outputsaver.configuration.productname.startswith("beam"):
        crc_expected = ["0x5f9f981e"]
    else:
        assert False, f"Unsupported productname: {outputsaver.configuration.productname}"

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(crc_expected)
    logging.info("HPGL2 bolly.wood_fastOFF_150_18x25.hpgl2 - Checksum(s) verified successfully")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file TEST.hpgl2 and check CRC
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-84162
    +timeout:350
    +asset:LFP
    +delivery_team:LFP
    +feature_team:ProductQA
    +test_framework:TUF
    +external_files:TEST.hpgl2=db4c3bb79af4c432d7cc053df0166fd1f9b74bf394e254d604f07b6afe90022b
    +test_classification:System
    +name:test_cals_print_and_check_CRC
    +test:
        +title:test_cals_print_and_check_CRC
        +guid:8b3d866d-b877-4d1d-81e6-df3cc7a8ff6a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_cals_print_and_check_CRC(setup_teardown, printjob, job, outputsaver, media):
    #NOTE: Not using parquimetre.cal=38020f0cf2cb8996a96b3115736cb6449eff1e41d7092fa2817445d9010476a6 
    #      as it is 46x60in and takes too much time
    outputsaver.operation_mode('CRC')

    ### Send the job
    printjob.print_verify('db4c3bb79af4c432d7cc053df0166fd1f9b74bf394e254d604f07b6afe90022b', 'SUCCESS', 300, 1)

    ### VERIFY
    if outputsaver.configuration.productname == "jupiter":
        crc_expected = ["0x95b92559"]
    else:
        crc_expected = ["0x3b6f9d3e"]
    outputsaver.save_output()
    outputsaver.verify_output_crc(crc_expected)

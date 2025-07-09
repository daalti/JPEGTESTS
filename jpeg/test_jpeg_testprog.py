import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg testprog Page from *testprog.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testprog.jpg=24770f706b81b40a71944af3b39aad8a3f7ffb21c4f2725447022e518222d823
    +test_classification:System
    +name:test_jpeg_testprog
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testprog
        +guid:a1d10fc7-b852-41b1-adf5-c5f2aef42b4c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testprog(setup_teardown, printjob, outputsaver, udw, cdm):
    expected_state = 'SUCCESS'

    response = cdm.get(cdm.CDM_MEDIA_CAPABILITIES)

    media_source= response['supportedInputs'][0]['mediaSourceId']
    resolution = response['supportedInputs'][0]['resolution']
    bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
    top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
    left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
    right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
    image_width=227/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
    image_height=149/600

    if("roll" in media_source):
        if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
            expected_state='FAILED'

    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('24770f706b81b40a71944af3b39aad8a3f7ffb21c4f2725447022e518222d823',expected_job_state=expected_state, timeout=120)
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG testprog Page- Print job completed successfully")


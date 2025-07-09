import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg testimg Page from *testimg.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testimg.jpg=ff6133bb58d3dae4f13ecbe05256dc4aaa05b17786b2c67f172cc3e934a00331
    +test_classification:System
    +name:test_jpeg_testimg
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testimg
        +guid:737fb68d-a637-4abb-bfab-e4452b83f640
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testimg(setup_teardown, printjob, outputsaver, cdm):

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

    printjob.print_verify('ff6133bb58d3dae4f13ecbe05256dc4aaa05b17786b2c67f172cc3e934a00331',expected_job_state=expected_state, timeout=120)
    outputsaver.save_output()

    logging.info("JPEG testimg Page- Print job completed successfully")

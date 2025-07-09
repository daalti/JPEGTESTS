import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg testimgp Page from *testimgp.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testimgp.jpg=e9486e697b7082a324fe2812310303e13b0ddf67b073eacb4b9d8a53e50b7ea7
    +test_classification:System
    +name:test_jpeg_testimgp
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testimgp
        +guid:d96aedb9-96e0-4f0d-804d-58d4515bd055
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testimgp(setup_teardown, printjob, outputsaver, cdm):

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

    printjob.print_verify('e9486e697b7082a324fe2812310303e13b0ddf67b073eacb4b9d8a53e50b7ea7',expected_job_state=expected_state, timeout=120)
    outputsaver.save_output()

    logging.info("JPEG testimgp Page- Print job completed successfully")

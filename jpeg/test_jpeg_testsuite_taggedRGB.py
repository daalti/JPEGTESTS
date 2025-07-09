import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite taggedRGB Page from *taggedRGB.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:taggedRGB.jpg=34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c
    +test_classification:System
    +name:test_jpeg_testsuite_taggedRGB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_taggedRGB
        +guid:418c892f-214e-4665-b773-86fbc78d7ed2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_taggedRGB(setup_teardown, printjob, outputsaver, cdm):
    expected_state = 'SUCCESS'

    response = cdm.get(cdm.CDM_MEDIA_CAPABILITIES)

    media_source= response['supportedInputs'][0]['mediaSourceId']
    resolution = response['supportedInputs'][0]['resolution']
    bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
    top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
    left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
    right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
    image_width=499/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
    image_height=202/600

    if("roll" in media_source):
        if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
            expected_state='FAILED'
    printjob.print_verify('34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c', expected_job_state=expected_state)
    outputsaver.save_output()

    logging.info("JPEG TestSuite taggedRGB Page - Print job completed successfully")
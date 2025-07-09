import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg testorig Page from *testorig.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testorig.jpg=acc6ec555d41d15b368320edaa3b20958ee6fa97cb6e4a18d1213d5ae8bec73b
    +test_classification:System
    +name:test_jpeg_testorig
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testorig
        +guid:33258d2f-aad2-4da9-858a-e040c7568692
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testorig(setup_teardown, printjob, outputsaver, udw, cdm):

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
    printjob.print_verify('acc6ec555d41d15b368320edaa3b20958ee6fa97cb6e4a18d1213d5ae8bec73b',expected_job_state=expected_state, timeout=120)
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("JPEG testorig Page- Print job completed successfully")

import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177632 IPP test for printing GreyscaleSource- greyscale image prints as color-composite grey
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:180
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__JPG_Source.pdf=321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0
    +test_classification:System
    +name:test_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey
    +test:
        +title:test_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey
        +guid:71a92a03-c54f-42f4-919b-b679ca70fde2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & PrintColorMode=Color
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_color_mode_greyscale_image_prints_as_color_composite_grey(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    ipp_test_file = '/code/tests/print/pdl/ipp/attributes/ColorOutputMode.test'
    printjob.ipp_print(ipp_test_file, '321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0')
    
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

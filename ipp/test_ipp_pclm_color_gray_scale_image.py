import pytest



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Ipp test for printing a PCL file using attribute value print-color-mode_process-monochrome
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__JPG_Source.pdf=321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0
    +name:test_ipp_pclm_color_gray_scale_image
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_color_gray_scale_image
        +guid:e423f497-d0e8-4f8c-bc00-8b90111defd4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_ipp_pclm_color_gray_scale_image(setup_teardown, printjob, outputsaver):
    ipp_test_attribs = {'document-format': 'application/PCLm', 'print-color-mode': 'monochrome','ipp-attribute-fidelity':'false'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
 
    printjob.ipp_print(ipp_test_file, '321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0')
    outputsaver.save_output()
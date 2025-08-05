import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile30.urf=572315252f6b3a53b576a7b678f22c2fe5e4fe40773d9c9f8ff33bda61e0e92d
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_RGB_duplex_nomedia_speci_file30
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_RGB_duplex_nomedia_speci_file30
        +guid:6048979d-3dc6-4f96-8a86-fd6e835f6439
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_deviceRGB_RGB_duplex_nomedia_speci_file30(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_deviceRGB_RGB_duplex_nomedia_speci_file30.test', '572315252f6b3a53b576a7b678f22c2fe5e4fe40773d9c9f8ff33bda61e0e92d')
    outputsaver.save_output()
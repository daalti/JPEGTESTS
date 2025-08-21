#ifndef DUNE_COPY_PIPELINEBUILDER_H
#define DUNE_COPY_PIPELINEBUILDER_H
////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConfigurablePipelineBuilder.h
 * @brief  CopyConfigurablePipelineBuilder for Copy jobs
 * @author Shubham Khandelwal
 * @date   2023-03-16
 *
 * (C) Copyright 2019 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "BaseColorTypes.h"
#include "ConvertToScanTypeHelper.h"
#include "CopyPipelineResourceSetup.h"
#include "CopyPipelineStandardConfig_generated.h"
#include "ICopyAdapter.h"
#include "ICopyJobTicket.h"
#include "ICopyPipelineBuilderAdapter.h"
#include "IImagePersister.h"
#include "IImageProcessor.h"
#include "IJobTicketHandler.h"
#include "ILayoutFilterTicket.h"
#include "IMarkingFilterTicket.h"
#include "IMediaAttributes.h"
#include "IPageAssembler.h"
#include "IPageAssemblerTicket.h"
#include "IPrintDevice.h"
#include "IPrintDeviceTicket.h"
#include "IResourceInstanceProxy.h"
#include "IResourceManagerClient.h"
#include "IResourceService.h"
#include "IRtpFilter.h"
#include "IScanDevice.h"
#include "IScanDeviceTicket.h"
#include "IIPADevice.h"
#include "IIPADeviceTicket.h"
#include "IScanPipeline.h"
#include "ImageContainer.h"
#include "JobFrameworkTypes.h"
#include "PipeQueueFactory.h"
#include "PipelineBuilder.h"
#include "ScanPipelineConfig_generated.h"
#include "IScanPipelineBuilder.h"
#include "ImageHandler.h"
#include "IResourceSetupHelper.h"
namespace dune { namespace imaging {
class IRasterFormatSelector;
class IPipelineMemoryClientCreator;
}}

namespace dune { namespace job {
class IIntentsManager;
}}

namespace dune { namespace print { namespace engine {
class IPrintIntentsFactory;
class IMedia;
}}}

namespace dune { namespace print { namespace engine { namespace helpers {
class IRenderingRequirements;
}}}}


namespace dune { namespace imaging { namespace color {
class IColorDirector;
}}}  // namespace dune::imaging::color

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::scan::Resources::IScanDeviceTicket;
using dune::imaging::Resources::IPageAssemblerTicket;
using dune::imaging::Resources::IMarkingFilterTicket;
using dune::print::Resources::IPrintDeviceTicket;
using dune::imaging::pipeobjects::imagecontainer::ImageContainer;
using dune::job::SegmentType;
using dune::job::PromptResponseType;
using dune::job::PromptType;
using dune::scan::types::ScanSource;
using dune::scan::Resources::IScanDeviceIntent;
using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;
using MarginsParameters = dune::print::engine::IMedia::MarginsParameters;
using Margins = dune::imaging::types::Margins;
using IDateTime = dune::framework::core::time::IDateTime;

class ICopyJobTicket;
using dune::job::IResourceManagerClient;
using dune::scan::Jobs::Scan::IScanPipeline;

class CopyConfigurablePipelineBuilder : public dune::job::PipelineBuilder<ICopyJobTicket, dune::job::IPipelineBuilder::Type::multiStage>
{
  public:
    CopyConfigurablePipelineBuilder(std::shared_ptr<ICopyJobTicket> ticket, const ServicesPackage& services,
                                    bool hasSharedPaperPath, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline,
                                    Product prePrintConfiguration, bool copyBasicPipeline,
                                    const MaxLengthConfig& maxLengthConfig, dune::job::IIntentsManager* intentsManager,
                                    IDateTime* dateTime, bool multiPageSupportedFromFlatbed,
                                    dune::copy::cdm::ICopyAdapter* copyApdater, bool layoutFilterEnabled);

    ResourceInstanceProxiesSection onInitialize() override;

    ResourceInstanceProxiesSection onBuildPipeline(PromptType promptType, PromptResponseType responseType,
                                                   SegmentType segmentType) override;

    void onJobCompletion(dune::job::JobCompletionPackage& completionPackage) override;

    /**
     * @brief hold pipeline releasing done resource and adding retriever and print device
     */
    void hold() override;

    /**
    * @brief interrupts pipeline releasing done resources and adding retriever and printdevice
    */
    void interrupt() override;

    /**
     * Methods needed to share information with the copy job ticket when ganerating scan page intent
     */ 

    /**
    * @brief get Default media size of copy job
    * @return  media size id
    */
    dune::imaging::types::MediaSizeId getDefaultMediaSize();
    
    /**
    * @brief get collate Mode of pipeline
    * @return  Collate mode
    */
    CollateMode getCollateMode() const;

    /**
    * @brief set the thresold override value
    * @param segment type
    */
    void setThresholdOverride(const int threshold) { thresholdOverride_ = threshold; };

    void setPipelineConfig(dune::scan::Jobs::Scan::PipelineBuilderConfigT* pipelineConfig);

    /**
    * @brief set the top specific padding override value
    * @param topSpecificPadding the specific padding to apply
    */

    void setTopSpecificPadding(float topSpecificPadding) { topSpecificPadding_ = topSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param bottomSpecificPadding the specific padding to apply
    */

    void setBottomSpecificPadding(float bottomSpecificPadding) { bottomSpecificPadding_ = bottomSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param leftSpecificPadding the specific padding to apply
    */

    void setLeftSpecificPadding(float leftSpecificPadding) { leftSpecificPadding_ = leftSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param rightSpecificPadding the specific padding to apply
    */

    void setRightSpecificPadding(float rightSpecificPadding) { rightSpecificPadding_ = rightSpecificPadding; };

    void setMaxPagesToCollate(uint32_t maxPagesToCollate) {maxPagesToCollate_ = maxPagesToCollate;};
    /**
    * @brief set the prnting order override value
    * @param printingOrder the printing order
    */
    void setPrintingOrder(dune::imaging::types::PrintingOrder printingOrder) { printingOrder_ = printingOrder; };    
    
    /**
    * @brief set the number of pages to wait before sequencing config value
    * @param pageCountBeforeSequencing the specific count to apply
    */
    void setPageCountBeforeSequencing(uint32_t pageCountBeforeSequencing) { pageCountBeforeSequencing_ = pageCountBeforeSequencing; };

    void setSimulatorJob(bool value) { simJob_ = value; };

    void applyPipelinePolicy();

    void setMaxFlatbedDuplexPages(uint32_t maxFlatbedDuplexPages ) { maxFlatbedDuplexPages_ = maxFlatbedDuplexPages; };

    uint32_t getMaxFlatbedDuplexPages() { return maxFlatbedDuplexPages_; };
      
   /**
    * @brief it returns  all resources of pipeline
    * @return collection of all proxies the pipelinebuilder uses
    */ 
    inline ResourceInstanceProxies getAllResources() { return allResources_; }
  
  private:

    const ServicesPackage&                                  services_;
    std::unique_ptr<CopyPipelineResourceSetup>              resourceSetup_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       scanDeviceInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       imageProcessorProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       imageProcessorPreviewProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       markingFilterInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>        layoutFilterInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       pageAssemblerInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       imagePersisterProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       imageRetrieverProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       bufferingImagePersisterProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       bufferingImageRetrieverProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       bufferingFinalSegmentImageRetrieverProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       rtpFilterProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       printDeviceInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       ipaDeviceInstanceProxy_;
    std::shared_ptr<dune::job::ResourceInstanceProxy>       imageImporterProxy_;
    std::shared_ptr<ICopyJobIntent>                         intent_;
    std::shared_ptr<ICopyJobTicket>                         ticket_;
    std::shared_ptr<dune::imaging::ImageHandler>            imageHandler_;
    

    
    // Copy pipeline configuration object 
    dune::scan::Jobs::Scan::PipelineBuilderConfigT*                       copyPipelineConfiguration_{nullptr};

    // Resource config list of particular segment 
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceConfig_;

    // Resource setup list passed to create pipeline
    std::vector<std::pair<dune::scan::Jobs::Scan::ResourceName, dune::scan::Jobs::Scan::IScanPipeline::ResourceDetails>>
        resourcesSetupList_;
    std::map<dune::scan::Jobs::Scan::ResourceName, 
      std::shared_ptr<dune::job::PipeQueue<ImageContainer>>>              persistedResourceList;

    dune::scan::Jobs::Scan::IScanPipeline*                                scanPipeline_{nullptr};
    dune::job::IIntentsManager*                                           intentsManager_{nullptr};
    dune::copy::cdm::ICopyAdapter*                                        copyAdapter_{nullptr};
    std::shared_ptr<dune::scan::Jobs::Scan::ScanPipelineConfigT>          scanPipelineConfig_{nullptr};
    
    dune::job::CompletionStateType                                        jobCompletionState_{dune::job::CompletionStateType::UNDEFINED};
    Product                                                               prePrintConfiguration_{Product::HOME_PRO};  ///< Print configuration value for copy pipeline
    SegmentType                                                           segmentType_{SegmentType::FinalSegment};
    
     std::vector<PipelineBuilderBase::ResourceInstanceProxies>            pipelineSections_{};
    std::string                                                           persistentPipePath_;
    const MaxLengthConfig&                                                maxLengthConfig_;
    int                                                                   numScanPages_{0};
    int                                                                   thresholdOverride_{0};
    bool                                                                  promptCanceled_{false};
    bool                                                                  previewJob_{false};
    bool                                                                  copyBasicPipeline_{false};
    bool                                                                  copyEnterprisePipeline_{false};
    bool                                                                  simJob_{true};
    bool                                                                  prescanJob_{false};
    bool                                                                  hasSharedPaperPath_{false};
    bool                                                                  useImagePersister_{false};
    bool                                                                  useImageProcessor_{false};
    bool                                                                  useMarkingFilter_{false};
    bool                                                                  useLayoutFilter_{false};
    float                                                                 topSpecificPadding_{0.0};
    float                                                                 bottomSpecificPadding_{0.0};
    float                                                                 leftSpecificPadding_{0.0};
    float                                                                 rightSpecificPadding_{0.0};
    uint32_t                                                              maxPagesToCollate_{0};
    uint32_t                                                              pageCountBeforeSequencing_{0};
    dune::job::PipelinePolicy                                             pipelinePolicy_{dune::job::PipelinePolicy::undefined};
    bool                                                                  isMultiplePrintJob_{false};
    dune::imaging::types::PrintingOrder                                   printingOrder_{dune::imaging::types::PrintingOrder::UNKNOWN};
    bool                                                                  multiPageSupportedFromFlatbed_{false};
    uint32_t                                                              maxFlatbedDuplexPages_{1};
    std::shared_ptr<dune::scan::Jobs::Scan::IScanPipelineBuilder>         scanPipelineBuilder_;
    std::shared_ptr<dune::scan::Jobs::Scan::IResourceSetupHelper>         resourceSetupHelper_;
    bool                                                                  layoutFilterEnabled_{false};
    bool                                                                  flatbedDuplexBackSide_{false};

  protected:

    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imagePersisterDiskBufferingConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageRetrieverDiskBufferingConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageRetrieverFinalDiskBufferingConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imagePersisterConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageRetrieverConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageProcessorConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> markingFilterConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> layoutFilterConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> scanDeviceConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> printDeviceConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> pageAssemblerConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> ipaDeviceConfig_;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageImporterConfig_;
    CollateMode                                                           collateMode_{CollateMode::NONE};
    // Stages
    Stage                                                                 currentStage_ = Stage::Setup;
    Stage                                                                 nextStage_ = Stage::Setup;

    /**
    * @brief Reads the passed segemnt's resource list from config file
    * @return Return list of reosurces.
    */
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> getResourceList(
        dune::scan::Jobs::Scan::PipelineSegmentType segmentType);
    
    /**
    * @brief populate the resource details and add them in the resource list with the there setup method
    * @param resourceList pass the resource list
    */
    void populateResourceDetails(std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList);

    /**
    * @brief setup the scan device ticket for scan resource
    * @param data it has the enqueue and dequeue
    */
    void setupScanDevice(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the scan device ticket for scan resource
    * @param data it has the enqueue and dequeue
    */
    void setupIPADevice(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the image processor ticket for image processor resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageProcessorTicket(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the marking filter ticket for marking filter resource
    * @param data it has the enqueue and dequeue
    */
    void setupMarkingFilter(IScanPipeline::PipeQueueInterface data);

    /**
     * @brief setup the layout filter ticket for layout filter resource
     * @param data it has the enqueue and dequeue
     */
    void setupLayoutFilter(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the page assembler ticket for page assembler resource
    * @param data it has the enqueue and dequeue
    */
    void setupPageAssembler(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the image persister ticket for image persister resource
    * @param data it has the enqueue and dequeue
    */
    void setupImagePersister(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageRetriever(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the buffer image persister ticket for image persiter resource
    * @param data it has the enqueue and dequeue
    */
    void setupBufferingImagePersister(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the buffer image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupBufferingImageRetriever(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the final buffering image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupFinalBufferingImageRetriever(IScanPipeline::PipeQueueInterface data);

    // /**
    // * @brief setup the image persiter preview ticket for image persister preview resource
    // * @param data it has the enqueue and dequeue
    // */
    // void setupImagePersisterPreview(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the image processor preview ticket for image processor resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageProcessorPreview(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the rtp filter ticket for rtp filter resource
    * @param data it has the enqueue and dequeue
    */
    void setupRtpFilterTicket(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief setup the print device ticket for print device resource
    * @param data it has the enqueue and dequeue
    */
    void setupPrintDevice(IScanPipeline::PipeQueueInterface data);

    /**
     * @brief setup the image importer ticket for image importer resource
     */
    void setupImageImporter(IScanPipeline::PipeQueueInterface data);

    /**
    * @brief set collate mode on the basis of job ticket setting
    */
    void setCollateMode();

    /**
    * @brief set first stage of the pipeline on the basis of the job ticket setting and configuration
    */
    void setFirstStage();

    /**
    * @brief fill the copy pipeline set setting in the job ticket, So, it can be used in print intent
    */
    void fillCopyPipelineJobTicketSettings();

    /**
    * @brief check if previous resource state is failed or not
    * @return return true value if preview resource is failed
    */
    bool isPreviousResourceStateFailed();

    /**
    * @brief reset allocated reources for next stage/segment
    */
    void resetAllocatedResources();

    /**
    * @brief resolve the condition and check if it is supported as per the job ticket, if yes return true
    * @param condition string value of condition
    * @return boolean value
    */
    bool resolveEnabledIfProperty(std::vector<std::string> conditions);

    /**
    * @brief get pre scanned width from scan device ticket
    * @return return width
    */
    uint32_t getPrescannedWidth();

    /**
    * @brief get pre scanned height from scan device ticket
    * @return return height
    */
    uint32_t getPrescannedHeight();

    /**
    * @brief update resource ticket by using intent Manager
    */
    void updateResourcesTicket();

    /**
    * @brief fill resource ticket for each resource type
    * @param resources resource list
    * @return retrun list of the resource ticket for each resource
    */
    std::vector<dune::job::IIntentsManager::ResourceTicket> fillResourcesTicket(const ResourceInstanceProxies &resources);

    /**
    * @brief handle response from prompt
    * @param responseType response from prompt
    */
    void handlePromptResponse(PromptResponseType responseType, PromptType promptType);

    void setJobName();

    void setResourceSetupConfiguration();

    void setCopyPipelineForNonEnterprise(PromptType promptType, PromptResponseType responseType,
                                                   SegmentType segmentType);
    

    void freeAllocatedResources();

    void setReourcesTrueForCollate();

    void setPrintingOrderForCollate();
    /**
     * @brief Free the kept done and allocated resources 
     */
    void freeDoneAllocatedResources();

    /**
     * @brief Find if a segment is on configuration
     *
     * @param segment Segment to find
     * @return Pointer to the segment if found, false otherwise
     */
    dune::scan::Jobs::Scan::CustomBuildPipelineT* findSegment(
        const dune::scan::Jobs::Scan::PipelineSegmentType& segment);

    /**
     * @brief Check if Layout Filter is needed for this job
     *
     * @param segment Segment to check if LayoutFilter is needed
     * @return true If LayoutFilter is needed, false otherwise
     */
    bool isLayoutFilterNeeded(const dune::scan::Jobs::Scan::PipelineSegmentType& segment);

    void populateJobTicketWithJobMetaInfo(std::shared_ptr<dune::job::IPipeMetaInfo> pipeMetaInfo);
};

}}}}  // namespace dune::copy::Jobs::Copy
#endif // DUNE_COPY_PIPELINEBUILDER_H

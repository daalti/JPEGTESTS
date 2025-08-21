#ifndef DUNE_JOB_COPYPAGEINTENT_H
#define DUNE_JOB_COPYPAGEINTENT_H
////////////////////////////////////////////////////////////////////////////////
/**
 * @file  CopyPageIntent.h
 * @brief Dune Job Pipeline - CopyPageIntent Class Definition
 * @date  April 14th, 2023
 *
 * (c) Copyright HP Inc. 2023. All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPageIntent_generated.h"
#include "PrintPageIntent.h"

namespace dune { namespace job {
/**
 * @class CopyPageIntent
 */

class CopyPageIntent 
{
    public:
      CopyPageIntent() :
        printPageIntent_{std::make_shared<dune::job::PrintPageIntent>()}
      {
      }
    
      inline std::shared_ptr<dune::job::PrintPageIntent> getPrintPageIntent() { return printPageIntent_;}

      /**
       * @brief Serialize / Deserialize Copy Page Ticket from/to FlatBuffer struct
       *
       * @return std::unique_ptr<CopyPageTicketFbT> Serialized Copy Page Ticket to FlatBuffer struct
       */
      inline std::unique_ptr<CopyPageIntentFbT> serializeToFb() const
      {
          std::lock_guard<std::recursive_mutex> lock_(mutex_);

          std::unique_ptr<dune::job::CopyPageIntentFbT> copyPageIntentFb{std::make_unique<dune::job::CopyPageIntentFbT>()};
          if(printPageIntent_)
          {
            copyPageIntentFb->printPageIntent = printPageIntent_->serializeIntent();
          }

          return copyPageIntentFb;
      }

      inline void deserializeFromFb(const CopyPageIntentFbT& copyPageIntentFb)
      {
          std::lock_guard<std::recursive_mutex> lock_(mutex_);

          printPageIntent_->deserializeIntent(*copyPageIntentFb.printPageIntent);
      }

    protected:
      std::shared_ptr<dune::job::PrintPageIntent> printPageIntent_{nullptr};
      mutable std::recursive_mutex mutex_; 
};

}}

#endif // DUNE_JOB_COPYPAGEINTENT_H
#pragma once

// Include for 'bool' type, as it's used in llama_backend_init
#include <stdbool.h>

// Standard llama.cpp API macro for cross-platform symbol export/import.
// If you are building llama.cpp as a static library, this might be defined
// as nothing. For a shared library, it handles __declspec(dllexport/dllimport)
// or __attribute__ ((visibility ("default"))).
// For simplicity in a self-contained header, we'll define a basic one if not already defined.
#ifndef LLAMA_API
#    ifdef LLAMA_SHARED
#        if defined(_WIN32) && !defined(__MINGW32__)
#            ifdef LLAMA_BUILD
#                define LLAMA_API __declspec(dllexport)
#            else
#                define LLAMA_API __declspec(dllimport)
#            endif
#        else
#            define LLAMA_API __attribute__ ((visibility ("default")))
#        endif
#    else
#        define LLAMA_API
#    endif
#endif

// Define llama_token_eos as it's common
#define llama_token_eos 2

#ifdef __cplusplus
extern "C" {
#endif

// Forward declaration of the opaque context struct
typedef struct llama_context llama_context;

// Struct for context parameters
typedef struct {
    int n_ctx;
    int n_threads;
    // Note: The actual llama_context_params struct in the official llama.cpp
    // is much more extensive. This is just based on your provided snippet.
} llama_context_params;


// --- Added new backend initialization and deinitialization functions ---

// Initializes the llama.cpp backend.
// Call this once at the very beginning of your application before any other llama_ functions.
// 'numa' (Non-Uniform Memory Access) attempts to enable NUMA support if true.
LLAMA_API void llama_backend_init(bool numa);

// Frees all global resources allocated by the llama.cpp backend.
// Call this once at the very end of your application.
LLAMA_API void llama_backend_free(void);

// --- End of added functions ---


// Existing function declarations from your snippet:
llama_context_params llama_context_default_params(void);
llama_context* llama_init_from_file(const char* path, llama_context_params params);
void llama_free(llama_context* ctx);

// IMPORTANT: The `llama_tokenize` and `llama_n_tokens` (from your CoreBrain)
// signatures are highly likely to be outdated for modern llama.cpp.
// Please double-check them against the llama.cpp version you are linking to.
// The current `llama_tokenize` in official llama.cpp typically fills a buffer
// and returns the number of tokens, rather than returning an `int*`.
// And `llama_n_tokens` is usually `llama_n_vocab` or `llama_n_ctx`.
int* llama_tokenize(llama_context* ctx, const char* text, bool add_bos);
int llama_eval(llama_context* ctx, const int* tokens, int n_tokens, int n_past, int n_threads);
const char* llama_token_to_str(llama_context* ctx, int token);
int llama_sample_top_p_top_k(llama_context* ctx, int top_k, float top_p, int n_batch, float temp, int repeat_penalty, const int* last_n_tokens);

#ifdef __cplusplus
}
#endif
#include <node.h>
#include <v8.h>

using namespace v8;

// Simple function that adds two numbers
void Add(const FunctionCallbackInfo<Value>& args) {
    Isolate* isolate = args.GetIsolate();
    Local<Context> context = isolate->GetCurrentContext();
    
    // Check if we have exactly 2 arguments
    if (args.Length() < 2) {
        isolate->ThrowException(Exception::TypeError(
            String::NewFromUtf8(isolate, "Wrong number of arguments").ToLocalChecked()));
        return;
    }
    
    // Check if arguments are numbers
    if (!args[0]->IsNumber() || !args[1]->IsNumber()) {
        isolate->ThrowException(Exception::TypeError(
            String::NewFromUtf8(isolate, "Arguments must be numbers").ToLocalChecked()));
        return;
    }
    
    // Get the arguments and perform addition
    double value1 = args[0]->NumberValue(context).FromJust();
    double value2 = args[1]->NumberValue(context).FromJust();
    double result = value1 + value2;
    
    // Return the result
    args.GetReturnValue().Set(Number::New(isolate, result));
}

// Function that calculates factorial
void Factorial(const FunctionCallbackInfo<Value>& args) {
    Isolate* isolate = args.GetIsolate();
    Local<Context> context = isolate->GetCurrentContext();
    
    if (args.Length() < 1 || !args[0]->IsNumber()) {
        isolate->ThrowException(Exception::TypeError(
            String::NewFromUtf8(isolate, "Argument must be a number").ToLocalChecked()));
        return;
    }
    
    int n = args[0]->Int32Value(context).FromJust();
    
    if (n < 0) {
        isolate->ThrowException(Exception::RangeError(
            String::NewFromUtf8(isolate, "Number must be non-negative").ToLocalChecked()));
        return;
    }
    
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    
    args.GetReturnValue().Set(Number::New(isolate, result));
}

// Context-aware initialization function
void Initialize(Local<Object> exports, Local<Value> module, Local<Context> context) {
    NODE_SET_METHOD(exports, "add", Add);
    NODE_SET_METHOD(exports, "factorial", Factorial);
}

// Use the context-aware module registration macro
NODE_MODULE_CONTEXT_AWARE(addon, Initialize)
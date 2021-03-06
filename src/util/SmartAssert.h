#pragma once

#include <string>

namespace kev {

class SmartAssert
{
public:
    SmartAssert(const std::string& expr) : SMART_ASSERT_A(*this), SMART_ASSERT_B(*this),
        expr_(expr), first_print_(true) {}
    
    SmartAssert& print_context(const std::string& file, int line) {
        printf("Failed: %s\nFile: %s, Line: %d\n", expr_.c_str(), file.c_str(), line);
        return *this;
    }
    
    template<class T>
    SmartAssert& print_value(const std::string& name, const T& value) {
        if(first_print_) {
            first_print_ = false;
            std::cout << "Context Variables:" << std::endl;
        }
        printf("\t %s=%s\n", name.c_str(), std::to_string(value).c_str());
        return *this;
    }
    
    static SmartAssert make_assert(const std::string& expr) {
        return SmartAssert(expr);
    }
    
    SmartAssert& SMART_ASSERT_A;
    SmartAssert& SMART_ASSERT_B;
    
private:
    std::string expr_;
    bool first_print_;
};

} // namespace kev

#define SMART_ASSERT_A(x) SMART_ASSERT_OP(x, B)
#define SMART_ASSERT_B(x) SMART_ASSERT_OP(x, A)
#define SMART_ASSERT_OP(x, next) SMART_ASSERT_A.print_value(#x, x).SMART_ASSERT_##next

#define SMART_ASSERT(expr) \
    if(expr) ; \
    else kev::SmartAssert::make_assert(#expr).print_context(__FILE__, __LINE__).SMART_ASSERT_A

// usage:
// SMART_ASSERT(expr)(val1)(val2)(val3)...(valn)

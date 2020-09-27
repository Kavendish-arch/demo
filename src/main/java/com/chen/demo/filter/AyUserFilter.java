package com.chen.demo.filter;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import java.io.File;
import java.io.IOException;

/**
 * @ClassName AyUserFilter
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/27 10:07
 * @Version 1.0
 */
@WebFilter(filterName = "ayUserFilter",urlPatterns = "/ayUser/*")
public class AyUserFilter implements Filter {
    
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("init Filter 初始化 过滤器");
    }
    
    @Override
    public void destroy() {
        System.out.println("destroy Filter  销毁过滤器");
    }
    
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("destroy Filter  销毁过滤器");
        // 放行
        filterChain.doFilter(servletRequest, servletResponse);
    }
}

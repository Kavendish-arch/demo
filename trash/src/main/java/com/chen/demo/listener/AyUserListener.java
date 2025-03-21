package com.chen.demo.listener;


import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;

/**
 * @ClassName AyUserListener
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/27 10:18
 * @Version 1.0
 */
@WebListener
public class AyUserListener implements ServletContextListener {
   
    private  static  final Logger logger = LogManager.getLogger(AyUserListener.class);
    
    @Override
    public void contextInitialized(ServletContextEvent sce) {
        
        logger.info("init Listener");
    }
    
    
    @Override
    public void contextDestroyed(ServletContextEvent sce) {
        logger.info("destroy Listener");
    }
}

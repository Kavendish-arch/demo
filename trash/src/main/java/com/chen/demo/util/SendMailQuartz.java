package com.chen.demo.util;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;



/**
 * @ClassName SendMailQuartz
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/27 11:36
 * @Version 1.0
 */
@Component
@Configuration
@EnableAutoConfiguration
public class SendMailQuartz {

    private static final Logger logger = LogManager.getLogger(SendMailQuartz.class);
    
    @Scheduled(cron = "*/5 * *   * * *")
    public void reportCurrentByCron(){
        logger.info("定时器运行了 !!!!");
    }
    
}

package com.chen.demo.controller;

import com.chen.demo.model.AyUser;
import com.chen.demo.service.AyUserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.annotation.Resource;
import java.util.List;

/**
 * @ClassName AyUserController
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/27 9:17
 * @Version 1.0
 */
@Controller
@RequestMapping("/ayUser")
public class AyUserController {
    
    @Resource
    private AyUserService ayUserService;
   
    @RequestMapping("/test")
    public String test(Model model) {
        List<AyUser> userList = ayUserService.findAll();
        model.addAttribute("users", userList);
        return "index";
    }
    
}

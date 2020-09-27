package com.chen.demo;

import com.chen.demo.model.AyUser;
import com.chen.demo.service.AyUserService;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.junit4.SpringRunner;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

/**
 * @ClassName MySqlTest
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/26 21:25
 * @Version 1.0
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class MySqlTest {

    @Resource
    private AyUserService ayUserService;
    
    @Test
    public void testRepository(){
        // 查询所有数据
        List<AyUser> userList = ayUserService.findAll();
        System.out.println("findAll: "+userList.size());
        for(AyUser ayUser : userList) {
            System.out.println(ayUser.toString());
        }
        
        // 通过 name 查询数据
        List <AyUser> user = ayUserService.findByName("Jack");
        System.out.println("findById: " + user.toString());
        // id 查询
        AyUser user1 = ayUserService.findById(3);
        System.out.println(user1.toString());
//        System.out.println("findById: " + user1.toString());
        AyUser ayUser = new AyUser();
        ayUser.setId(3);
//        ayUserService.delete(ayUser);
        List <AyUser> user2 = ayUserService.findByNameLike("%ack%");
        System.out.println("模糊查询" + user2.toString());
       
        List<Integer> ids = new ArrayList<>();
        ids.add(1);
        ids.add(2);
        List<AyUser> userList1 = ayUserService.findByIdIn(ids);
        System.out.println("findIdsIn: " + userList1.toString());
    
        PageRequest pageRequest = new PageRequest(0,10);
        Page<AyUser> userPage = ayUserService.findAll(pageRequest);
        Assert.assertTrue(userPage.getSize()==10);
        System.out.println("page : ");
        for (AyUser ayUser1 : userPage) {
            System.out.println(ayUser1.toString());
        }
//        Assert.assertTrue("断言",1==2);
    }
    @Test
    public void saveUser(){
        AyUser ayUser = new AyUser();
        ayUser.setId(22);
        ayUser.setUsername("李伟");
        ayUser.setPassword("12345");
        System.out.println( ayUserService.save(ayUser));
    }
   
    @Test
    public void findByNameAndPassword(){
        
        System.out.println( ayUserService.findByNameAndPassword("chen","dd"));
    }
    
    
}

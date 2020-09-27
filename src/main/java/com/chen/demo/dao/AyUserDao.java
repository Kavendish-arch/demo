package com.chen.demo.dao;

import com.chen.demo.model.AyUser;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

/**
 * @ClassName AyUserDao
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/27 11:10
 * @Version 1.0
 */
@Mapper
//@Repository
public interface AyUserDao {
    
    /**
     * 根据用户名和密码查找用户
     * @param name
     * @param password
     * @return
     */
    AyUser findByNameAndPassword(@Param("name") String name,
                                 @Param("password") String password);
}

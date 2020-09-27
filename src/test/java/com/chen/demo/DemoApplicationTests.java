package com.chen.demo;

import com.chen.demo.model.AyUser;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.test.context.junit4.SpringRunner;

import javax.annotation.Resource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@RunWith(SpringRunner.class)
@SpringBootTest
public class DemoApplicationTests {

    @Resource
    private JdbcTemplate jdbcTemplate;
    
    @Test
    public void contextLoads() {
        System.out.println("hello world");
    }
    
    @Test
    public void mySqlTest() {
        String sql = "select * from user";
        List<AyUser> list = (List<AyUser>) jdbcTemplate.query(sql, new RowMapper<AyUser>() {
    
            @Override
            public AyUser mapRow(ResultSet resultSet, int i) throws SQLException {
                AyUser user = new AyUser();
                user.setId(resultSet.getInt("id"));
                user.setUsername(resultSet.getString("username"));
                user.setPassword(resultSet.getString("password"));
                return user;
            }
        });
        System.out.println("query successfully ");
        for (AyUser user : list) {
            System.out.println(user.toString());
        }
    }
    
    
}

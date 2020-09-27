package com.chen.demo.model;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * @ClassName AyUser
 * @Description TODO
 * @Author newChenyingtao
 * @Date 2020/9/26 21:27
 * @Version 1.0
 */

@Entity
@Table(name = "user")
public class AyUser {
    @Id
    private Integer id;
    private String username;
    private String password;
    
    @Override
    public String toString() {
        return "AyUser{" +
                       "id=" + id +
                       ", username='" + username + '\'' +
                       ", password='" + password + '\'' +
                       '}';
    }
    
    public Integer getId() {
        return id;
    }
    
    public void setId(Integer id) {
        this.id = id;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
}

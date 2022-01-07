package com.example.mvvmapp

import androidx.test.platform.app.InstrumentationRegistry
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.example.mvvmapp.ui.auth.Validator

import org.junit.Test
import org.junit.runner.RunWith

import org.junit.Assert.*

/**
 * Instrumented test, which will execute on an Android device.
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest {
    @Test
    fun useAppContext() {
        // Context of the app under test.
        val appContext = InstrumentationRegistry.getInstrumentation().targetContext
        assertEquals("com.example.mvvmapp", appContext.packageName)
    }
    @Test
    fun signUpInputValidation(){
        val username = "gulsah"
        val password = "1234"
        val passwordConfirm = "1234"
        val email = "xx@gmail.com"

        val result = Validator.validateUserSignUp(username,password,email,passwordConfirm)
        assertTrue(result)
    }

    @Test
    fun signUpUserNameEmpty(){
        val username = ""
        val password = "1234"
        val passwordConfirm = "1234"
        val email = "xx@gmail.com"

        val result = Validator.validateUserSignUp(username,password,email,passwordConfirm)
        assertFalse(result)
    }

    @Test
    fun signUpPasswordDontMatch(){
        val username = "gulsah"
        val password = "12345"
        val passwordConfirm = "1234"
        val email = "xx@gmail.com"

        val result = Validator.validateUserSignUp(username,password,email,passwordConfirm)
        assertFalse(result)
    }

    @Test
    fun signUpEmailEmpty(){
        val username = "gulsah"
        val password = "12345"
        val passwordConfirm = "1234"
        val email = ""

        val result = Validator.validateUserSignUp(username,password,email,passwordConfirm)
        assertFalse(result)
    }

    @Test
    fun signUpPasswordEmpty(){
        val username = "gulsah"
        val password = ""
        val passwordConfirm = ""
        val email = "xx@gmail.com"

        val result = Validator.validateUserSignUp(username,password,email,passwordConfirm)
        assertFalse(result)
    }

    @Test
    fun loginPasswordEmpty(){
        val username = "gulsah"
        val password = ""

        val result = Validator.validateUserLogin(username,password)
        assertFalse(result)
    }

    @Test
    fun loginUsernameEmpty(){
        val username = ""
        val password = "1234"

        val result = Validator.validateUserLogin(username,password)
        assertFalse(result)
    }
}
// src/components/RouteGuard.tsx
"use client";

import { useState, useEffect } from "react";
import { routes, protectedRoutes } from "@/app/resources";
import { useClientPathTracker } from "@/hooks/useClientPathTracker";
import { Flex, Spinner, Button, Heading, Column, PasswordInput } from "@/once-ui/components";
import NotFound from "@/app/not-found";

interface RouteGuardProps {
  children: React.ReactNode;
}

const RouteGuard: React.FC<RouteGuardProps> = ({ children }) => {
  const pathname = useClientPathTracker(); // ✅ 추적 경로 상태 훅
  const [isRouteEnabled, setIsRouteEnabled] = useState(false);
  const [isPasswordRequired, setIsPasswordRequired] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | undefined>(undefined);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!pathname) return;

    const performChecks = async () => {
      setLoading(true);
      setIsRouteEnabled(false);
      setIsPasswordRequired(false);
      setIsAuthenticated(false);
      setError(undefined);

      const checkRouteEnabled = (path: string): boolean => {
        if (path in routes) return routes[path as keyof typeof routes];
        const dynamicRoutes = ["/blog", "/work"] as const;
        return dynamicRoutes.some((route) => path.startsWith(route) && routes[route]);
      };

      const routeEnabled = checkRouteEnabled(pathname);
      setIsRouteEnabled(routeEnabled);

      if (protectedRoutes[pathname as keyof typeof protectedRoutes]) {
        setIsPasswordRequired(true);

        try {
          const response = await fetch("https://api.joshuatech.dev/security/check-auth", {
            method: "GET",
            credentials: "include",
          });
          setIsAuthenticated(response.ok);
        } catch (err) {
          console.error("❌ 인증 확인 실패:", err);
        }
      }

      setLoading(false);
    };

    performChecks();
  }, [pathname]);

  const handlePasswordSubmit = async () => {
    try {
      const response = await fetch("https://api.joshuatech.dev/security/authenticate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ password }),
      });

      if (response.ok) {
        setIsAuthenticated(true);
        setError(undefined);
      } else {
        setError("Incorrect password");
      }
    } catch (err) {
      setError("Network error");
    }
  };

  if (loading) {
    return (
      <Flex fillWidth paddingY="128" horizontal="center">
        <Spinner />
      </Flex>
    );
  }

  if (!isRouteEnabled) {
    return <NotFound />;
  }

  if (isPasswordRequired && !isAuthenticated) {
    return (
      <Column paddingY="128" maxWidth={24} gap="24" center>
        <Heading align="center" wrap="balance">
          This page is password protected
        </Heading>
        <Column fillWidth gap="8" horizontal="center">
          <PasswordInput
            id="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            errorMessage={error}
          />
          <Button onClick={handlePasswordSubmit}>Submit</Button>
        </Column>
      </Column>
    );
  }

  return <>{children}</>;
};

export { RouteGuard };
